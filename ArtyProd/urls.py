"""
URL configuration for ArtyProd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from service.views import add_blog_comment, add_comment, homePageView

from service import views

urlpatterns = [path('admin/', admin.site.urls),
               path("", include("service.urls")),
               path('', homePageView, name='home'),
               path('blog/<int:id>', views.single_blog_view, name='single_blog'),
               path('blog/<int:blog_id>/add_blog_comment/',add_blog_comment, name='add_blog_comment'),
               path('about/', views.about_view, name='about'),
               path('pricing/', views.pricing_view, name='pricing'),
               path('blog/', views.blog_item, name='blog'),
               path('services/', views.servicesPageView, name='services'),
               path('teams/', views.teams_view, name='teams'),
               path('team/<str:id>/', views.team_view, name='team'),
               path('portfolio/<int:id>/', views.portfolio_detail,
                    name='detail_portfolio'),
               path('portfolio/<int:id>/add_comment/',
                    views.add_comment, name='add_comment'),
               path('portfolio/', views.portfolio_view, name='portfolio'),
               path('register/', views.RegistrationView.as_view(), name='register'),
               path(
                   'login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
               path(
                   'logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
               path('contact/', views.contact_view, name='contact'),
               path('request/', views.create_project,
                    name='request'),



               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
