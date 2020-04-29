"""pdoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
        path("get-doctors/",views.get_doctors,name="get_doctors"),
        path("get-telecall-doctors/",views.get_telecalldoctors,name="get_telecalldoctors"),
        path("doctors/",views.search,name="doctors"),
        path("signup/",views.signup_customer,name="signup_customer"),
        path("signup-action/",views.signup_customer_action,name="signup_customer_action"),
        path("doctor-registration/",views.doctor_registration,name="doctor_registration"),
        path("doctor-registration-action/",views.doctor_registration_action,name="doctor_registration_action"),
        path("details/",views.details,name="details"),
        path("important-links/",views.important_links,name="important_links"),
        path("",views.doctors_over_call,name="doctors_over_call"),
        path("",views.index,name="index"),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
