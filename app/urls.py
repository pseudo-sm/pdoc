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
from django.conf.urls import (handler400, handler403, handler404, handler500, url)
from django.conf import settings
from .sitemaps import CategorySitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'categories': CategorySitemap
}


urlpatterns = [
        path("cms/",views.cms,name="cms"),
        path("login-action/",views.login_action,name="login_action"),
        path("update-cms/",views.update_cms,name="update_cms"),
        path("update-cms-image/",views.cms_image,name="update_cms_image"),
        path("logout/",views.logout,name="logout"),
        path("about-us/",views.about,name="about_us"),
        path("diagnostic-cat/",views.diagnostic_cat,name="diagnostic_cat"),
        path("get-doctors/",views.get_doctors,name="get_doctors"),
        path("get-diagnostics/",views.get_diagnostic_cat,name="get_diagnostics"),
        path("re-request/",views.re_request,name="re_request"),
        path("get-telecall-doctors/",views.get_telecalldoctors,name="get_telecalldoctors"),
        path("doctors/",views.doctors,name="doctors"),
        path("physical-consultation/",views.physical_consultation,name="physical_consultation"),
        path("new-physical-consultation/",views.new_physical_appointment,name="new_physical_appointment"),
        path("doctors/<slug:slug>",views.doctor_pages,name="doctor_pages"),
        path("paramedics/<slug:slug>",views.paramedic_pages,name="paramedic_pages"),
        path("doctors-cat/",views.doctors_cat,name="doctors_cat"),
        path("paramedics-cat/",views.paramedics_cat,name="paramedics_cat"),
        path("paramedics/",views.paramedics,name="paramedics"),
        path("signup/",views.signup_customer,name="signup_customer"),
        path("articles/",views.blog_list,name="blog_list"),
        path("article/<slug:slug>",views.blog_single,name="blog_single"),
        path("signup-action/",views.signup_customer_action,name="signup_customer_action"),
        path("doctor-registration/",views.doctor_registration,name="doctor_registration"),
        path("doctor-registration-action/",views.doctor_registration_action,name="doctor_registration_action"),
        path("details/",views.details,name="details"),
        path("health-and-fitness-advisor-signup/",views.paramedic_health_and_fitness_advisor,name="paramedic_health_and_fitness_advisor"),
        path("health-and-fitness-advisor-action/",views.paramedic_health_and_fitness_advisor_action,name="paramedic_health_and_fitness_advisor_action"),
        path("yoga-guru-signup/",views.paramedic_yoga_guru,name="paramedic_yoga_guru"),
        path("yoga-guru-action/",views.paramedic_yoga_guru_action,name="paramedic_yoga_guru_action"),
        path("physiotherapy-action/",views.paramedic_physiotherapy_action,name="paramedic_physiotherapy_action"),
        path("clinical-psychiatry-signup/",views.paramedic_clinical_pscyhiatry,name="paramedic_clinical_pscyhiatry"),
        path("clinical-psychiatry-action/",views.paramedic_clinical_pscyhiatry_action,name="paramedic_clinical_pscyhiatry_action"),
        path("physiotherapy-signup/",views.paramedic_physiotherapy,name="paramedic_physiotherapy"),
        path("physiotherapy-action/",views.paramedic_clinical_pscyhiatry_action,name="paramedic_physiotherapy_action"),
        path("drug-house-signup/",views.paramedic_drug_house,name="paramedic_drug_house"),
        path("drug-house-action/",views.paramedic_drug_house_action,name="paramedic_drug_house_action"),
        path("diagnostics-signup/",views.paramedic_diagnostics,name="paramedic_diagnostics"),
        path("diagnostics-action/",views.paramedic_diagnostics_action,name="paramedic_diagnostics_action"),
        path("important-links/",views.important_links,name="important_links"),
        path("doctors-over-call/",views.doctors_over_call,name="doctors_over_call"),
        path("login/",views.login,name="login"),
        path("zonal-admin/",views.zonal_admin,name="zonal_admin"),
        path("zonal-admin-settlements/",views.zonal_admin_settlements,name="zonal_admin_settlements"),
        path("zonal-admin-doctors/",views.zonal_admin_doctors,name="zonal_admin_doctors"),
        path("done-appointment/",views.done_appointment,name="done_appointment"),
        path("patient-dashboard/",views.patient_dashboard,name="patient_dashboard"),
        path("doctor-wait/<slug:slug>",views.doctor_wait,name="doctor_wait"),
        path("video-calling/<slug:slug>",views.video_calling,name="video_calling"),
        path("request-video-calling/",views.request_video_calling,name="request_video_calling"),
        path("terms-and-conditions",views.terms,name="terms"),
        path("privacy-policy",views.privacy_policy,name="privacy_policy"),
        path("refund-policy",views.refund_policy,name="refund_policy"),
        path("book-appointment/",views.book_appointment,name="book_appointment"),
        path("appointment-close/",views.appointment_close,name="appointment_close"),
        path("book-appointment-paramedic/",views.book_appointment_paramedic,name="book_appointment_paramedic"),
        path("payment-booking/",views.payment_booking,name="payment_booking"),
        path("payment/",views.payment,name="payment"),
        path("payment-status/",views.payment_status,name="payment_status"),
        path("download-prescription/<slug:prescription>",views.create_prescription_document,name="create_prescription_document"),
        path("prescription-submit/",views.prescription_submit,name="prescription_submit"),
        path("feedback/<slug:meeting>",views.feedback,name="feedback"),
        path("feedback-submit/",views.feedback_submit,name="feedback_submit"),
        path("statistics/",views.statistics,name="statistics"),
        path("email-contact-form/",views.email_contact_form,name="email_contact_form"),
        path("new-lead/",views.new_lead,name="new_lead"),
        path("shop/<slug:name>",views.product_item,name="product_item"),
        path("",views.index,name="index"),




        path("zonal-admin-new/",views.zonal_admin_new,name="zonal_admin_new"),
]
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = views.handler404
handler500 = views.handler500
