"""Elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from Elearning import views
from .views import sociallogin
from allauth.socialaccount.views import ConnectionsView
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/',TemplateView.as_view(template_name='home.html'),name='home'),
   # path('social/',views.sociallogin),
   # path('slogin/', ConnectionsView.as_view(template_name='social_login.html'), name='social_login'),

    # path('otp/', views.mail,name='otp'),
    # path('check_otp',views.check_otp,name='check_otp'),
    # path("check_otp/", views.check_otp, name="check_otp"),
    # #path("", views.login, name="login"),
    # #path("", views.logout, name="logout"),
     path("",views.celerys, name="celery"),
    # path("home/", views.schedule_mail, name="home"),
    # path("edit/", views.edit, name="edit"),
    # path("registerteacher/", views.register_as_teacher, name="registert"),
    # path("registerstudent/", views.register_as_student, name="registers"),
    # path("delete/<str:pk>", views.delete, name="delete"),
    # path("update/<str:pk>", views.update, name="update"),
    # path("purchase/<str:pk>", views.purchase, name="purchase"),
    # path("content/<str:pk>", views.content, name="content"),
    # path("addcontent/<str:pk>", views.addcontent, name="addcontent"),
    # path("deletecontent/<str:pk>", views.deletecontent, name="deletecontent"),
    # path("purchaselist/<str:pk>", views.purchaselist, name="purchaselist"),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
