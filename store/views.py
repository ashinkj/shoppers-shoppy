from django.shortcuts import render
# from django.http import HttpResponse

def home(request):
    
    return render(request,"store/home.html")

def store(request):
    return render(request,"store/store.html")

def cart(request):
    return render(request,"store/cart.html")

def checkout(request):
    return render(request,"store/checkout.html")
