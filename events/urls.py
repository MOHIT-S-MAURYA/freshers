from . import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('packages/', views.packages, name='packages'),
    path('profile/', views.profile, name='profile'),
    path('book/', views.book_view, name='book'),
    path('get_package_options/<int:package_id>/', views.get_package_options, name='get_package_options'),

]

