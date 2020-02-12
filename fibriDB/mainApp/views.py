from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework import viewsets, status, generics
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from mainApp.models import items
from mainApp.serializers import ItemsSerializer, UserSerializer
from mainApp import forms


class mainView(View):
    output = {}

    def get(self, request, output=output):
        output.update({'message': "HEYO"})
        return render(request, 'mainApp/index.html', output)


# Handling multiple items
class ItemList(APIView):
    def get(self, request, format=None):
        item = items.objects.all()  # Get all items
        serializer = ItemsSerializer(item, many=True)  # Serialize the items with the defined attributes
        return Response(serializer.data)  # Return the serialized data as JSON

    def post(self, request, format=None):
        serializer = ItemsSerializer(data=request.data)  # Serialize the received items with the defined attributes
        if serializer.is_valid():
            serializer.save()  # Save the received items to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handling a single item
class ItemDetail(APIView):
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class userAccount(View):
    def get(self, request):
        form = forms.UserProfileInfoForm
        return render(request, 'mainApp/useraccount.html', {'form': form})
