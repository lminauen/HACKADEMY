from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from mainApp.models import items
from mainApp.serializers import ItemsSerializer
from mainApp.forms import UserProfileInfoForm


class mainView(View):
    output = {}

    def get(self, request, output=output):
        output.update({'message': "HEYO"})
        return render(request, 'mainApp/index.html', output)


@csrf_exempt
def item_list(request):
    """
    List all items, or create a new item.
    """
    if request.method == 'GET':
        item = items.objects.all()
        serializer = ItemsSerializer(item, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ItemsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def item_detail(request, pk):
    """
    Retrieve, update or delete an item.
    """
    try:
        item = items.objects.get(pk=pk)
    except item.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ItemsSerializer(item)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ItemsSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return HttpResponse(status=204)


class userAccount(View):
    def get(self, request):
        form = forms.UserProfileInfoForm
        return render(request, 'mainApp/useraccount.html', {'form': form})


