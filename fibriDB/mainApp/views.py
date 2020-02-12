from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework import viewsets, status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from mainApp.models import items
from mainApp.serializers import ItemsSerializer


class mainView(View):
    output = {}

    def get(self, request, output=output):
        output.update({'message': "HEYO"})
        return render(request, 'mainApp/index.html', output)


# Handling multiple items
@api_view(['GET', 'POST'])  # Only allow GET and POST requests
def item_list(request):
    if request.method == 'GET':
        item = items.objects.all()  # Get all items
        serializer = ItemsSerializer(item, many=True)  # Serialize the items with the defined attributes
        return Response(serializer.data)  # Return the serialized data as JSON

    elif request.method == 'POST':
        serializer = ItemsSerializer(data=request.data)  # Serialize the received items with the defined attributes
        if serializer.is_valid():
            serializer.save()  # Save the received items to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handling a single item
@api_view(['GET', 'PUT', 'DELETE'])  # Only allow GET, POST and DELETE requests
def item_detail(request, pk):
    try:
        item = items.objects.get(pk=pk)  # Get the item corresponding to the received primary key
    except item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemsSerializer(item)  # Serialize the item with the defined attributes
        return Response(serializer.data)  # Return the serialized data as JSON

    elif request.method == 'PUT':
        serializer = ItemsSerializer(item, data=request.data)  # Serialize the received item with the defined attributes
        if serializer.is_valid():
            serializer.save()  # Save the received item to DB
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()  # Delete the item from the DB
        return Response(status=status.HTTP_204_NO_CONTENT)
