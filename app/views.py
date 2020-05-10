from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import datetime
from django.contrib import auth
import json
from django.db import IntegrityError
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
    all_links = Links.objects.all()
    return render(request,"index.html",{"links":all_links})

def search(request):
    area = Area.objects.all()
    type = Type.objects.all()
    return render(request,"search.html",{"areas":area,"types":type})

def details(request):

    return render(request,"details.html")

def doctors_over_call(request):
    type = Type.objects.filter(status=True)
    terms = Others.objects.get(name="terms")
    print(terms)
    return render(request,"telecalling.html",{"types":type,"terms":terms})

def get_telecalldoctors(request):

    doctors = TeleCallDoctors.objects.filter(status=True)
    all_doctors = doctors.values("name","type_id__name","education","practicing_year","direct_contact","phone","designation","hospital","address")
    if request.GET.get("type") == "0":
        for doctor in all_doctors:
            if not doctor["direct_contact"]:
                doctor["phone"] = "8917240913"
        return JsonResponse(list(all_doctors),safe=False)
    type = request.GET.get("type")
    filtered_doctors = doctors.filter(type=type).values("name","type_id__name","education","practicing_year","direct_contact","phone","designation","hospital","address")
    print(filtered_doctors)
    for doctor in filtered_doctors:
        print(doctor["direct_contact"])
        if not doctor["direct_contact"]:
            doctor["phone"] = "8917240913"
    return JsonResponse(list(filtered_doctors),safe=False)

def doctor_registration(request):

    return render(request,"signup.html")

def doctor_registration_action(request):
    name = request.GET.get("name")
    hospital = request.GET.get("hospital")
    type = request.GET.get("specialization")
    phone = request.GET.get("phone")
    designation = request.GET.get("designation")
    location = request.GET.get("location")
    from1 = request.GET.get("from")
    to = request.GET.get("to")
    id = request.GET.get("id")
    if len(Type.objects.filter(name=type)) == 0:
        type = Type(name=type,description=type)
        type.save()
    else:
        type = Type.objects.get(name=type)
    new_doc = TeleCallDoctors(name=name,hospital=hospital,type=type,phone=phone,designation=designation,address=location,available_from=from1,available_to=to,registration_id=id)
    new_doc.save()
    return JsonResponse(True,safe=False)

def important_links(request):

    links = Links.objects.all()
    return render(request,"important-links.html",{"links":links})

def signup_customer(request):

    return render(request,"sign-up-customer.html")

def signup_customer_action(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    phone = request.GET.get("phone")
    password = request.GET.get("password")
    query = request.GET.get("query")
    try:
        user = User.objects.create_user(username=email,password=password)
    except IntegrityError:
        return JsonResponse({"error":True,"message" : "You have already Signed Up with us"})
    auth.login(request,user=user)
    new_customer = Customer(name=name,phone=phone,query=query,user_id=user)
    new_customer.save()
    return JsonResponse(True,safe=False)

def paramedic_health_and_fitness_advisor(request):
    return render(request,"paramedics/health-and-fitness-advisor.html")

def paramedic_health_and_fitness_advisor_action(request):
    name = request.GET.get("name")
    qualification = request.GET.get("qualifications")
    designation = request.GET.get("designation")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    available_from = request.GET.get("from")
    available_to = request.GET.get("to")
    achievements = request.GET.get("achievements")
    about = request.GET.get("about")
    new_paramedic_health_and_fitness_advisor = HealthFitnessAdvisor(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,achievements=achievements,available_to=available_to,available_from=available_from,about=about)
    new_paramedic_health_and_fitness_advisor.save()
    return JsonResponse(True,safe=False)

def paramedic_yoga_guru(request):

    return render(request,"paramedics/yoga-guru.html")

def paramedic_yoga_guru_action(request):
    name = request.GET.get("name")
    qualification = request.GET.get("qualifications")
    organization = request.GET.get("organization")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    available_from = request.GET.get("from")
    available_to = request.GET.get("to")
    achievements = request.GET.get("achievements")
    about = request.GET.get("about")
    new_paramedic_yoga_guru = YogaGuru(name=name,qualifications=qualification,address=address,available_to=available_to,available_from=available_from,phone=phone,achievements=achievements,about=about,organization=organization)
    new_paramedic_yoga_guru.save()
    return JsonResponse(True,safe=False)

def paramedic_physiotherapy(request):

    return render(request,"paramedics/physiotherapy.html")

def paramedic_physiotherapy_action(request):
    name = request.GET.get("name")
    qualification = request.GET.get("qualifications")
    designation = request.GET.get("designation")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    available_from = request.GET.get("from")
    available_to = request.GET.get("to")
    achievements = request.GET.get("achievements")
    about = request.GET.get("about")
    organization = request.GET.get("organization")
    new_physiotherapist = Physiotherapist(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,available_from=available_from,available_to=available_to,achievements=achievements,about=about,organization=organization)
    new_physiotherapist.save()
    return JsonResponse(True,safe=False)

def paramedic_clinical_pscyhiatry(request):

    return render(request,"paramedics/clinical-psychiatry.html")

def paramedic_clinical_pscyhiatry_action(request):
    name = request.GET.get("name")
    qualification = request.GET.get("qualifications")
    designation = request.GET.get("designation")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    available_from = request.GET.get("from")
    available_to = request.GET.get("to")
    achievements = request.GET.get("achievements")
    about = request.GET.get("about")
    organization = request.GET.get("organization")
    new_clinical_psychiatrist = ClinicalPsychiatry(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,available_from=available_from,available_to=available_to,achievements=achievements,about=about,organization=organization)
    new_clinical_psychiatrist.save()
    return JsonResponse(True,safe=False)

def paramedic_drug_house(request):

    return render(request,"paramedics/drug-house.html")

def paramedic_drug_house_action(request):
    name = request.GET.get("name")
    license = request.GET.get("license")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    about = request.GET.get("about")
    new_drug_house = DrugHouse(name=name,license_no=license,address=address,phone=phone,about=about)
    new_drug_house.save()
    return JsonResponse(True,safe=False)

def paramedic_diagnostics(request):

    return render(request,"paramedics/diagnostics.html")

def paramedic_diagnostics_action(request):
    name = request.GET.get("name")
    pickup = request.GET.get("pickup")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    if pickup=="Yes":
        pickup = True
    else:
        pickup=False
    new_diagnostic = Diagnostics(name=name,collection=pickup,address=address,phone=phone)
    new_diagnostic.save()
    return JsonResponse(True,safe=False)

def fitness_advisor_show(request):
    health_advisor = HealthFitnessAdvisor.objects.all()
    return render(request,"paramedics-show/fitness-advisors.html",{"health_advisor":health_advisor})

def physiotherapist_show(request):
    physiotherapist = Physiotherapist.objects.all()
    return render(request,"paramedics-show/physiotherapist.html",{"physiotherapists":physiotherapist})

def clinical_psychiatry_show(request):
    clinical_psychiatry = ClinicalPsychiatry.objects.all()
    return render(request,"paramedics-show/clinical-psychiatry.html",{"clinical_psychiatrys":clinical_psychiatry})

def diagonistic_show(request):
    diagonistics = Diagnostics.objects.all()
    return render(request,"paramedics-show/diagnostics.html",{"diagonistics":diagonistics})

def yoga_guru_show(request):
    yoga_gurus = YogaGuru.objects.all()
    return render(request,"paramedics-show/yoga-guru.html",{"yoga_gurus":yoga_gurus})

def pharamacies_show(request):
    pharmacies = DrugHouse.objects.all()
    return render(request,"paramedics-show/drughouse.html",{"pharmacies":pharmacies})
