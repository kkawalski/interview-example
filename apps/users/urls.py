from django.urls import path

from apps.users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),
] 
