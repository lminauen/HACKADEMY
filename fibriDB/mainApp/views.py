# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import permissions
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from mainApp import forms
from mainApp.models import items, UserProfileInfo
from mainApp.permissions import IsCreatorOrReadOnly
from mainApp.serializers import ItemsSerializer, UserSerializer, NearestItemSerializer
import math
from decimal import *


# Create your views here.
def index(request):
    return render(request, 'mainApp/index.html', )


class mainView(View):
    output = {}

    def get(self, request, output=output):
        output.update({'message': "HEYO"})
        return render(request, 'mainApp/index.html', output)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('mainApp:user-list'),
        'items': reverse('mainApp:item-list')
    })


# Handling multiple items
class ItemList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        item = items.objects.all()  # Get all items
        serializer = ItemsSerializer(item, many=True)  # Serialize the items with the defined attributes
        return Response(serializer.data)  # Return the serialized data as JSON

    def post(self, request, format=None):
        serializer = ItemsSerializer(data=request.data)  # Serialize the received items with the defined attributes
        if serializer.is_valid():
            serializer.save(user=self.request.user)  # Save the received items to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handling a single item
class ItemDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]

    def get_object(self, pk):
        try:
            return items.objects.get(pk=pk)  # Get the item corresponding to the received primary key
        except items.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemsSerializer(item)  # Serialize the item with the defined attributes
        return Response(serializer.data)  # Return the serialized data as JSON

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemsSerializer(item, data=request.data)  # Serialize the received item with the defined attributes
        if serializer.is_valid():
            serializer.save()  # Save the received item to DB
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()  # Delete the item from the DB
        return Response(status=status.HTTP_204_NO_CONTENT)


class NearestItems(APIView):
    def get(self, request, format=None):
        type = int(self.request.GET.get('type'))
        number = int(self.request.GET.get('number'))
        lat = Decimal(self.request.GET.get('lat'))
        lng = Decimal(self.request.GET.get('lng'))

        item_dist = []

        for item in items.objects.filter(type=type):
            d_lat = lat - item.latitude
            d_lng = lng - item.longitude

            temp = (
                    math.sin(d_lat / 2) ** 2
                    + math.cos(item.latitude)
                    * math.cos(lat)
                    * math.sin(d_lng / 2) ** 2
            )

            distance_m = 6373000 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))  # Distance in meters
            item_dist.append([item, distance_m])

        item_dist.sort(key=lambda x: x[1], reverse=False)

        item_list = [i[0] for i in item_dist[0:number]]
        id_dist = dict([(p[0].id, p[1]) for p in item_dist[0:number]])

        serializer = NearestItemSerializer(item_list, many=True, context={'id_dist': id_dist})

        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'mainApp/index.html', {})


class userAccount(View):
    def get(self, request):
        user = forms.UserForm
        form = forms.UserProfileInfoForm
        return render(request, 'mainApp/useraccount.html', {'user_form': user, 'profile_form': form})


def register(request):
    registered = False
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid and profile_form.is_valid:

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    return render(request, 'mainApp/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'mainApp/index.html', {})
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to login, but failed miserably')
            print('Username: {} and password {}'.format(username, password))
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request, 'fibriDB/login.html', {})


@login_required
def edit_profile(request):
    print("I am running")
    # print(UserProfileInfo.objects.get(pk=request.user.id))
    # profile = UserProfileInfo.objects.get(pk=request.user.id)
    # form = forms.UserProfileInfoForm(instance=profile)
    UserForm = forms.UserForm(instance=request.user)
    args = {}
    if request.method == 'POST':
        print("I AM RETURNING")
        form = forms.UserForm(request.POST, instance=request.user)
        if form.is_valid():
            print("I AM RETURNING")
            form.save()
            # profile = UserProfileInfo.objects.get(pk=request.user.id)
            # form = forms.UserProfileInfoForm(instance=profile)
            UserForm = forms.UserForm(instance=request.user)
            # args['form'] = form
            args['UserForm'] = UserForm
            print("I AM RETURNING")
            return render(request, 'mainApp/editprofile.html', args)
        else:

            return render(request, 'mainApp/editprofile.html')
    else:
        # args.update(csrf(request))
        # args['form'] = form
        args['UserForm'] = UserForm
        # args['profile_form'] = profile_form
        return render(request, 'mainApp/editprofile.html', args)


@login_required
def edit_item(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.UserProfileInfoForm(request.POST, request.FILES,
                                                 instance=request.user.userprofileinfo)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('mainApp:editprofile')
    else:
        form = forms.ItemForm(instance=request.user)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'accounts/editprofile.html', args)


@login_required
def edit_item(request):
    if request.method == 'POST':
        form = forms.ItemForm(request.POST, instance=request.items)

        if form.is_valid():
            item_form = form.save()
            return redirect('mainApp:editprofile')
    else:
        form = forms.ItemForm(instance=request.user)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        return render(request, '../templates/mainApp/edititem.html', {'item_form': items, 'item_form': form})
