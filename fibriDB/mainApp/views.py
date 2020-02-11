from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.


class mainView(View):
    output = {}

    def get(self, request, output=output):
        output.update({'message': "HEYO"})
        return render(request, 'mainApp/index.html', output)
