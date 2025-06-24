from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def dashboard_page(request): 
    return render(request, 'dashboard.html')

def cadastro_page(request):
    return render(request, 'cadastro.html')

def ia_page(request):
    return render(request, 'ia.html')