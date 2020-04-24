from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import datetime
import json
from django.contrib.postgres.search import SearchVector
# Create your views here.

def get_doctors(request):
    doctors = Doctor.objects.all()
    if request.GET.get("type") == "0":
        return JsonResponse(list(doctors.values("name","type_id__name","image","education","practicing_year")),safe=False)
    areas = request.GET.get("areas")
    education = request.GET.get("education")
    keyword = request.GET.get("keyword")
    type = request.GET.get("type")
    experience = request.GET.get("experience")
    areas = json.loads(areas)
    area = Area.objects.get(id=areas[0])
    filtered_doctors = doctors.filter(area=area)
    for area in areas:
        area = Area.objects.get(id=area)
        filtered_doctors = filtered_doctors | doctors.filter(area=area)
    filtered_doctors = filtered_doctors.filter(type=type)
    filtered_doctors = filtered_doctors.filter(name__icontains=keyword)

    now = datetime.datetime.now()
    for doc in filtered_doctors:
        if int(now.year)-int(doc.practicing_year) < int(experience):
            filtered_doctors = filtered_doctors.exclude(id=doc.id)
    return JsonResponse(list(filtered_doctors.values("name","type_id__name","image","education","practicing_year")),safe=False)

def index(request):

    return render(request,"index.html")

def search(request):
    area = Area.objects.all()
    type = Type.objects.all()
    return render(request,"search.html",{"areas":area,"types":type})

def details(request):

    return render(request,"details.html")

def doctors_over_call(request):
    type = Type.objects.all()
    return render(request,"telecalling.html",{"types":type})

def get_telecalldoctors(request):

    doctors = TeleCallDoctors.objects.all()
    if request.GET.get("type") == "0":
        return JsonResponse(list(doctors.values("name","type_id__name","education","practicing_year","direct_contact","phone")),safe=False)
    type = request.GET.get("type")
    experience = request.GET.get("experience")
    filtered_doctors = doctors.filter(type=type)
    now = datetime.datetime.now()
    for doc in filtered_doctors:
        if int(now.year)-int(doc.practicing_year) < int(experience):
            filtered_doctors = filtered_doctors.exclude(id=doc.id)
    return JsonResponse(list(filtered_doctors.values("name","type_id__name","education","practicing_year","direct_contact","phone")),safe=False)
