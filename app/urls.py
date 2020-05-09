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
        path("health-and-fitness-advisor-signup/",views.paramedic_health_and_fitness_advisor,name="paramedic_health_and_fitness_advisor"),
        path("health-and-fitness-advisor-action/",views.paramedic_health_and_fitness_advisor_action,name="paramedic_health_and_fitness_advisor_action"),
        path("yoga-guru/",views.paramedic_yoga_guru,name="paramedic_yoga_guru"),
        path("yoga-guru-action/",views.paramedic_yoga_guru_action,name="paramedic_yoga_guru_action"),
        path("physiotherapy-action/",views.paramedic_physiotherapy_action,name="paramedic_physiotherapy_action"),
        path("clinical-psychiatry/",views.paramedic_clinical_pscyhiatry,name="paramedic_clinical_pscyhiatry"),
        path("clinical-psychiatry-action/",views.paramedic_clinical_pscyhiatry_action,name="paramedic_clinical_pscyhiatry_action"),
        path("physiotherapy/",views.paramedic_physiotherapy,name="paramedic_physiotherapy"),
        path("physiotherapy-action/",views.paramedic_clinical_pscyhiatry_action,name="paramedic_physiotherapy_action"),
        path("drug-house/",views.paramedic_drug_house,name="paramedic_drug_house"),
        path("drug-house-action/",views.paramedic_drug_house_action,name="paramedic_drug_house_action"),
        path("diagnostics/",views.paramedic_diagnostics,name="paramedic_diagnostics"),
        path("diagnostics-action/",views.paramedic_diagnostics_action,name="paramedic_diagnostics_action"),
        path("important-links/",views.important_links,name="important_links"),
        path("doctors-over-call/",views.doctors_over_call,name="doctors_over_call"),
        path("health-and-fitness-advisors/",views.fitness_advisor_show,name="fitness_advisor_show"),
        path("",views.index,name="index"),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
