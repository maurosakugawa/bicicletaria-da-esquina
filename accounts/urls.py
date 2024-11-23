from django.urls import path
from accounts.views import dashboard_view  # Import correto da view desejada
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),  # Use a view correta
]
