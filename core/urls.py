from django.urls import path
from . import views

urlpatterns = [
    # O '' significa a raiz (ex: http://127.0.0.1:8000/)
    path('login/', views.login_page, name='home'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('cadastro/', views.cadastro_page, name='cadastro'),
]