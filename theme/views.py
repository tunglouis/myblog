from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.
def homepage(request):
    return TemplateResponse(request, 'index.html')