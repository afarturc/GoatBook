from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def post(request):
    return render(request, "post.html")
