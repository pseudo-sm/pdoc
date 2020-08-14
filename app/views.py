import random
import string
import os

from django.db.models import Q
from django.views.static import serve
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.utils.timezone import utc
import razorpay
from django.views.decorators.csrf import csrf_exempt
from docx.shared import Cm
from docxtpl import DocxTemplate

from .models import *
import datetime
from django.contrib import auth
import json
from django.db import IntegrityError
from django.contrib.postgres.search import SearchVector
# Create your views here.
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
doctor_types = Type.objects.filter(type_category=1)
paramedic_types = Type.objects.filter(type_category=2)
client = razorpay.Client(auth=("rzp_live_7VShD4pzdX6r0m", "HFFXrT0KRIObgzB7SvU7JdZG"))

import pyrebase

config = {
  "apiKey": "AIzaSyCNtuLp9_8dTKGHGnYTQDvtc4sjdG6Al8Q",
  "authDomain": "pdochealth.firebaseapp.com",
  "databaseURL": "https://pdochealth.firebaseio.com",
  "storageBucket": "pdochealth.appspot.com"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response

def get_doctors(request):
    doctors = Doctor.objects.all()
    if request.GET.get("type") == "0":
        print(doctors)
        return JsonResponse(list(doctors.values("name","type_id__name","image","education","practicing_year","special_day","special_from","special_to")),safe=False)
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
    print(filtered_doctors)
    return JsonResponse(list(filtered_doctors.values("name","type_id__name","image","education","practicing_year","special_day","special_from","special_to")),safe=False)

def search(request):
    area = Area.objects.all()
    type = Type.objects.all()
    return render(request,"search.html",{"areas":area,"types":type})

def details(request):

    return render(request,"details.html")

def doctors_over_call(request):
    type = Type.objects.all()
    terms = Others.objects.get(name="terms")
    return render(request,"telecalling.html",{"types":type,"terms":terms})

def doctors(request):
    type = Type.objects.filter(type_category="1")
    terms = Others.objects.get(name="terms")
    return render(request,"doctors.html",{"types":type,"terms":terms,"doctor_types":doctor_types,"paramedic_types":paramedic_types})

def doctors_cat(request):
    category = request.GET.get("category")
    type_service = request.GET.get("type")
    if category != "all":
        type = Type.objects.get(id=int(category))
        if type_service is None:
            doctors = Doctor.objects.filter(type=type)
        elif type_service=="telecall":
            doctors = Doctor.objects.filter(type=type,telecalling=True)
        elif type_service=="videocall":
            doctors = Doctor.objects.filter(type=type,videoconferencing=True)
    else:
        if type_service is None:
            doctors = Doctor.objects.all()
        elif type_service=="telecall":
            doctors = Doctor.objects.filter(telecalling=True)
        elif type_service=="videocall":
            doctors = Doctor.objects.filter(videoconferencing=True)
    doctors = doctors.values("id","name","type_id__name","education","practicing_year","direct_contact","phone","designation","hospital","address","available_from","available_to","available_from2","available_to2","special_day","special_from","special_to","fees")
    for doctor in doctors:
        doctor["available_from"] = doctor["available_from"].strftime("%H:%M")
        doctor["available_to"] = doctor["available_to"].strftime("%H:%M")
        if doctor["available_from2"] is not None:
            doctor["available_from2"] = doctor["available_from2"].strftime("%H:%M")
            doctor["available_to2"] = doctor["available_to2"].strftime("%H:%M")
        if doctor["special_day"] is not None:
            doctor["special_from"] = doctor["special_from"].strftime("%H:%M")
            doctor["special_to"] = doctor["special_to"].strftime("%H:%M")
        doctor["fees"] = str(int(doctor["fees"])+int(int(doctor["fees"])*0.12))
    return JsonResponse(list(doctors),safe=False)

def paramedics_cat(request):
    category = request.GET.get("category")
    if category != "all":
        type = Type.objects.get(id=int(category))
        paramedics = Paramedics.objects.filter(type=type,)
    else:
        paramedics = Paramedics.objects.all()
    paramedics = paramedics.values("id","name","type_id__name","qualifications","achievements","organization","phone","designation","address","available_from","available_to")
    for paramedic in paramedics:
        if paramedic["available_from"] is None:
            paramedic["available_from"] = "Available Time Slots"
            paramedic["available_to"] = "Not Mentioned"
    return JsonResponse(list(paramedics),safe=False)


def doctor_pages(request,slug):
    category = slug.replace("-"," ")
    type = Type.objects.filter(type_category="1")
    terms = Others.objects.get(name="terms")
    this_type = Type.objects.get(name=category)
    doctors = Doctor.objects.filter(type=this_type)
    return render(request,"doctors-pages.html",{"types":type,"terms":terms,"doctor_types":doctor_types,"paramedic_types":paramedic_types,"req_category":this_type.id})

def paramedic_pages(request,slug):
    category = slug.replace("-"," ")
    type = Type.objects.filter(type_category="2")
    terms = Others.objects.get(name="terms")
    this_type = Type.objects.get(name=category)
    paramedics = Paramedics.objects.filter(type=this_type)
    return render(request,"paramedics-pages.html",{"types":type,"terms":terms,"doctor_types":doctor_types,"paramedic_types":paramedic_types,"req_category":this_type.id})


def paramedics(request):
    type = Type.objects.filter(type_category="2")
    terms = Others.objects.get(name="terms")
    print(terms)
    return render(request,"paramedics.html",{"types":type,"terms":terms,"doctor_types":doctor_types,"paramedic_types":paramedic_types})


def get_telecalldoctors(request):

    doctors = Doctor.objects.filter(status=True)
    all_doctors = doctors.values("name","type_id__name","education","practicing_year","direct_contact","phone","designation","hospital","address","available_from","available_to")
    print(all_doctors)
    if request.GET.get("type") == "0":
        for doctor in all_doctors:
            if not doctor["direct_contact"]:
                doctor["phone"] = "8917240913"
            if doctor["available_from"] is None:
                doctor["available_from"] = "Available Time Slots"
                doctor["available_to"] = "Not Mentioned"
        return JsonResponse(list(all_doctors),safe=False)
    type = request.GET.get("type")
    filtered_doctors = doctors.filter(type=type).values("name","type_id__name","education","practicing_year","direct_contact","phone","designation","hospital","address","available_from","available_to")
    print(filtered_doctors)
    for doctor in filtered_doctors:
        print(doctor["direct_contact"])
        if not doctor["direct_contact"]:
            doctor["phone"] = "8917240913"
    return JsonResponse(list(filtered_doctors),safe=False)

def doctor_registration(request):

    return render(request,"signup.html",{"doctor_types":doctor_types,"paramedic_types":paramedic_types})

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
    new_doc = Doctor(name=name,hospital=hospital,type=type,phone=phone,designation=designation,address=location,available_from=from1,available_to=to,practice_id=id)
    new_doc.save()
    return JsonResponse(True,safe=False)

def important_links(request):

    links = Links.objects.all()
    return render(request,"important-links.html",{"links":links,"doctor_types":doctor_types,"paramedic_types":paramedic_types})

def signup_customer(request):
    if request.user.is_authenticated:
        return redirect("/patient-dashboard/")
    terms = Terms.objects.all()
    terms = terms.last()
    return render(request,"sign-up-customer.html",{"doctor_types":doctor_types,"paramedic_types":paramedic_types,"terms":terms})


def payment(request):
    order_id=request.GET.get("order_id")
    customer = Customer.objects.get(razor_pay_order_id=order_id)
    name = customer.name
    phone = customer.phone
    user_id = customer.user_id
    order_id = customer.razor_pay_order_id
    payment_id = customer.payment_id
    signature_id = customer.signature_id
    date = datetime.datetime.now().strftime("%m/%d/%Y")
    return render(request,"payment.html",{"name":name,"phone":phone,"username":user_id,"date":date,"order_id":order_id,"signature_id":signature_id,"payment_id":payment_id})

def payment_booking(request):
    order_id=request.GET.get("order_id")
    appointment = Appointments.objects.get(razor_pay_order_id=order_id)
    customer = appointment.customer
    name = customer.name
    phone = customer.phone
    user_id = customer.user_id
    date = datetime.datetime.now().strftime("%m/%d/%Y")
    return render(request,"payment-booking.html",{"order_id":order_id,"name":name,"phone":phone,"username":user_id,"date":date,"fees":int(int(appointment.doctor.fees)*1.12),"slug":appointment.slug})


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
    new_customer = Customer(name=name,phone=phone,query=query,user_id=user,email=email,password=password)
    new_customer.save()
    new_customer.save()
    body = "Hi {}, Welcome to Pdochealth by Edoc Medical Services Pvt Ltd\n Our Customer Relation Representative will contact you shortly. Meanwhile please go through the website to checkout our sservices.".format(name)
    email_msg = EmailMessage("Welcome to Pdochealth", body, settings.EMAIL_HOST_USER,
                             ["saswathcommand@gmail.com",email])
    email_msg.send(fail_silently=False)
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
    type = Type.objects.get(name="Health and Fitness Advisor")
    new_paramedic_health_and_fitness_advisor = Paramedics(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,achievements=achievements,available_to=available_to,available_from=available_from,about=about,type=type)
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
    type = Type.objects.get(name="Yoga Guru")
    new_paramedic_yoga_guru = Paramedics(name=name,qualifications=qualification,address=address,available_to=available_to,available_from=available_from,phone=phone,achievements=achievements,about=about,organization=organization,type=type)
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
    type = Type.objects.get(name="Physiotherapist")
    new_physiotherapist = Paramedics(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,available_from=available_from,available_to=available_to,achievements=achievements,about=about,organization=organization,type=type)
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
    type = Type.objects.get(name="Clinical Therapist")
    new_clinical_psychiatrist = Paramedics(name=name,qualifications=qualification,designation=designation,address=address,phone=phone,available_from=available_from,available_to=available_to,achievements=achievements,about=about,organization=organization,type=type)
    new_clinical_psychiatrist.save()
    return JsonResponse(True,safe=False)

def paramedic_drug_house(request):
    type = Type.objects.filter(status=True)
    terms = Others.objects.get(name="terms")
    return render(request,"paramedics/drug-house.html")

def paramedic_drug_house_action(request):
    name = request.GET.get("name")
    license = request.GET.get("license")
    address = request.GET.get("location")
    phone = request.GET.get("phone")
    about = request.GET.get("about")
    type = Type.objects.get(name="Drug House")
    new_drug_house = Paramedics(name=name,license_no=license,address=address,phone=phone,about=about,type=type)
    new_drug_house.save()
    type = Type.objects.filter(status=True)
    terms = Others.objects.get(name="terms")
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
    type = Type.objects.get(name="Diagnostics")
    new_diagnostic = Paramedics(name=name,collection=pickup,address=address,phone=phone,type=type)
    new_diagnostic.save()
    return JsonResponse(True,safe=False)


def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    customer = Customer.objects.filter(email=email,password=password)
    if len(customer)>0:
        customer = customer.first()
        user = auth.authenticate(request,username=email,password=password)
        auth.login(request,user)
    else:
        messages.error(request, f"Invalid Username or password")
        return redirect("/signup/")
    return redirect("/patient-dashboard/")

@login_required(login_url="signup_customer")
def patient_dashboard(request):
    customer = Customer.objects.get(user_id=request.user.id)
    not_yet=request.GET.get("not_time")
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user_id=user)
    scheduled_appointments = Appointments.objects.filter(customer=customer,status__gte="1")
    prescriptions = Prescription.objects.filter(appointment__customer=customer)
    scheduled_appointments=scheduled_appointments.values("doctor__name","doctor__type__name","doctor__hospital","time","slug","status","datetime")
    shortlisted_scheduled_appointments = []
    for appointment in scheduled_appointments:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        delta = now - appointment["time"]
        print("timedelta : ------------------------------")
        if delta.days < 30 :
            shortlisted_scheduled_appointments.append(appointment)
    vdoctor = len(list(Doctor.objects.filter(videoconferencing=True)))
    tdoctor = len(list(Doctor.objects.filter(telecalling=True)))
    pmconsultancy = len(list(Paramedics.objects.filter()))
    if not_yet is not None:
        return render(request,"customer/dashboard.html",{"p":"true","vdoctor":vdoctor,"tdoctor":tdoctor,"pmconsultancy":pmconsultancy,"doctor_types":doctor_types,"paramedic_types":paramedic_types,"scheduled_appointments":shortlisted_scheduled_appointments,"logout":True,"prescriptions":prescriptions,"cprescription":len(prescriptions)})
    return render(request,"customer/dashboard.html",{"vdoctor":vdoctor,"tdoctor":tdoctor,"pmconsultancy":pmconsultancy,"doctor_types":doctor_types,"paramedic_types":paramedic_types,"scheduled_appointments":shortlisted_scheduled_appointments,"logout":True,"prescriptions":prescriptions,"cprescription":len(prescriptions)})

def blog_list(request):
    articles = Article.objects.all()
    return render(request,"blog-list.html",{"articles":articles,"doctor_types":doctor_types,"paramedic_types":paramedic_types})

def blog_single(request,slug):
    article = Article.objects.get(slug=slug)
    return render(request,"blog-single.html",{"article":article,"doctor_types":doctor_types,"paramedic_types":paramedic_types})

def zonal_admin(request):
    appointments = Appointments.objects.filter(Q(status="0") | Q(status="3"))
    # paramedic_bookings = ParamedicBookings.objects.filter(status="0")
    appointments = appointments.values("id","name","phone","datetime","doctor__name","doctor__phone","query","type","status","payment_status")
    for row in appointments:
        print(row["payment_status"],row["id"])
    return render(request,"Zonal Admin/index.html",{"appointments":appointments[::-1]})

def zonal_admin_doctors(request):
    doctors = Doctor.objects.all()
    doctors = doctors.values("practice_id","name","address","education","phone","type__name","available_from","available_to","available_from2","available_to2","designation","hospital","special_day","special_from","special_to")
    return render(request,"Zonal Admin/doctors.html",{"doctors":doctors})

def video_calling(request,slug):
    appointment = Appointments.objects.get(slug=slug)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    name = appointment.doctor.name
    practice_id = appointment.doctor.practice_id
    designation = appointment.doctor.designation
    delta = appointment.time - now
    print(delta)
    if request.user.is_authenticated:
        doctor = False
    else:
        doctor = True
    minutes = (delta.seconds//60)
    customer = appointment.customer.id
    if minutes < 20 or now > appointment.time:
        return render(request,"videocalling.html",{"doctor":doctor,"name":name,"practice_id":practice_id,"designation":designation,"customer":customer})
    return redirect("/patient-dashboard/?not_time=true")

def request_video_calling(request):
    doctor = request.GET.get("doctor")
    patient = request.user.id
    print(doctor,patient)
    return JsonResponse(True,safe=False)


def get_doctor_categories(request):
    doctor_types = Type.objects.filter(type_category=1)
    print(doctor_types)
    return JsonResponse(True,safe=False)

def terms(request):
    terms = Others.objects.get(name="terms")
    all_links = Links.objects.all()
    return render(request,"terms.html",{"terms":terms,"links":all_links,"doctor_types":doctor_types,"paramedic_types":paramedic_types})

def book_appointment(request):
    if request.user.is_authenticated:
        doctor = request.GET.get("doctor")
        name = request.GET.get("name")
        phone = request.GET.get("phone")
        query = request.GET.get("query")
        type = request.GET.get("type")
        doctor = Doctor.objects.get(id=doctor)
        customer_id = request.user.id
        user = User.objects.get(id=customer_id)
        customer = Customer.objects.get(user_id=user)
        slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        data = {
            "amount" : int(doctor.fees)*112,
            "currency" : "INR",
            "receipt" : "1",
            "payment_capture" : 1,

        }
        order_id = client.order.create(data=data)
        new_appointment = Appointments(doctor=doctor,name=name,phone=phone,query=query,type=type,customer=customer,slug=slug)
        new_appointment.razor_pay_order_id=order_id["id"]
        new_appointment.save()
        doctor_name = doctor.name
        patient_name = customer.name
        phone = customer.phone
        email_notify(patient_name,doctor_name,phone)
        return JsonResponse({"order_id":order_id},safe=False)
    else:
        return JsonResponse(False,safe=False)

def book_appointment_paramedic(request):
    if request.user.is_authenticated:
        paramedic = request.GET.get("paramedic")
        name = request.GET.get("name")
        phone = request.GET.get("phone")
        query = request.GET.get("query")
        type = request.GET.get("type")
        paramedic = Paramedics.objects.get(id=paramedic)
        new_appointment = ParamedicBookings(paramedic=paramedic,name=name,phone=phone,query=query,type=type)
        new_appointment.save()
        return JsonResponse(True,safe=False)
    return JsonResponse(False,safe=False)
import datetime
def done_appointment(request):
    id = request.GET.get("id")
    type = request.GET.get("type")
    datetime_str = request.GET.get("datetime")
    date = datetime_str.split(" ")[0].split("-")
    time = datetime_str.split(" ")[1].split(":")
    year,month,date = int(date[0]),int(date[1]),int(date[2])
    hour,minute = int(time[0]),int(time[1])
    datetime_obj = datetime.datetime(year,month,date,hour,minute,0,0)
    print(datetime_obj)
    if type=="doctor":
       appointment = Appointments.objects.get(id=id)
       appointment.status="1"
       appointment.time=datetime_obj
       appointment.save()
    else:
        appointment = ParamedicBookings.objects.get(id=id)
        appointment.status="1"
        appointment.save()
    return JsonResponse(True,safe=False)

def appointment_close(request):
    appointment = request.GET.get("appointment")
    appointment = Appointments.objects.get(slug=appointment)
    appointment.count=int(appointment.count)+1
    appointment.status="2"
    appointment.save()
    prescription = Prescription.objects.filter(appointment=appointment).first()
    print(prescription)
    return JsonResponse({"prescription":prescription.slug},safe=False)

def logout(request):
    auth.logout(request)
    return redirect('/signup/')


@csrf_exempt
def payment_action(request):
    order_id = request.POST.get("order_id")
    customer = Customer.objects.get(razor_pay_order_id=order_id)
    return signup_customer(request)


def payment_status(request):
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")
    payment_id = request.GET.get("payment_id")
    appointment = Appointments.objects.get(razor_pay_order_id=order_id)
    appointment.payment_id=payment_id
    appointment.signature_id=signature
    try:
        client.utility.verify_payment_signature({"razorpay_signature":signature,"razorpay_order_id":order_id,"razorpay_payment_id":payment_id})
        appointment.payment_status=True
    except:
        appointment.payment_status=False
    appointment.save()
    return JsonResponse(appointment.payment_status,safe=False)

def email_notify(patient,doctor,phone):
    body = "A user name {} wants an appointment with Dr. {}".format(patient,doctor)
    email_msg = EmailMessage("Important!! PDOC - You Have a New Appointment Request", body, settings.EMAIL_HOST_USER, ["saswathcommand@gmail.com"])
    email_msg.send(fail_silently=False)
    return JsonResponse(True,safe=False)

def prescription_submit(request):
    medicines = request.GET.get("medicines")
    summary = request.GET.get("summary")
    roomhash = request.GET.get("roomhash")
    medicines = json.loads(medicines)
    appointment = Appointments.objects.get(slug=roomhash)
    slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    if request.GET.get("resave")=="true":
        prescription = request.GET.get("prescription")
        print("-"*20)
        print(prescription)
        prescription = Prescription.objects.get(pk=prescription)
        prescription.summary = summary
        Medicine.objects.filter(prescription_id=prescription).delete()
    else:
        prescription = Prescription(appointment=appointment,summary=summary,slug=slug)
    prescription.save()
    for medicine in medicines:
        new_medicine = Medicine(prescription_id=prescription,medicine=medicine["medicine"],morning=medicine["m"],lunch=medicine["l"],evening=medicine["s"],dinner=medicine["d"],afterFood=medicine["aftFood"],period=medicine["period"],quantity=medicine["quantity"],remarks=medicine["remark"])
        new_medicine.save()
    filepath = save_prescription(prescription)
    save_prescription_firebase(filepath,appointment.customer.id)
    return JsonResponse({"prescription":prescription.pk},safe=False)

def save_prescription(prescription):

    appointment = prescription.appointment
    customer = appointment.customer.id
    medicine_list = []
    medicines = Medicine.objects.filter(prescription_id=prescription)
    sl = 1
    doctor_id = appointment.doctor.practice_id
    for medicine in medicines:
        temp = {
                    "sl":str(sl),
                    "name":medicine.medicine,
                    "remark":medicine.remarks,
                    "quantity":medicine.quantity,
                    "period":medicine.period,
                }
        if medicine.afterFood:
            food = "After Food"
        else:
            food = "Before Food"
        maen = []
        if medicine.morning:
            maen.append("morning")
        if medicine.lunch:
            maen.append("afternoon")
        if medicine.evening:
            maen.append("evening")
        if medicine.dinner:
            maen.append("dinner")
        temp.update({"maen":",".join(maen),"food":food})
        medicine_list.append(temp)
        sl = sl+1
    context = {

        'date': prescription.datetime.strftime("%d %B, %Y"),
        'doctor_id': doctor_id,
        'medicines': medicine_list,
        'summary': prescription.summary,
    }
    print(context)
    count = appointment.count

    # tpl = DocxTemplate("/home/pdochealth/pdoc/app/template.docx")
    # tpl.render(context)
    # name = "prescription-"+str(appointment.id)+"-"+str(count)+".docx"
    # filepath = '/home/pdochealth/pdoc/app/prescriptions/'+name

    tpl = DocxTemplate("app/template.docx")
    tpl.render(context)
    name = "prescription-"+str(appointment.id)+"-"+str(prescription.pk)+".docx"
    filepath = 'app/prescriptions/'+name

    tpl.save(filepath)
    return filepath

def save_prescription_firebase(filename,customer):
    name = filename.split("/")[-1]
    storage.child("records/{}/{}".format(customer,name)).put(filename)

def create_prescription_document(request,prescription):
    prescription  = Prescription.objects.get(slug=prescription)
    filepath = save_prescription(prescription)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-docx")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
            return response
    raise Http404


def re_request(request):

    appointment = request.GET.get("appointment")
    appointment = Appointments.objects.get(slug=appointment)
    appointment.status = "3"
    appointment.save()
    return JsonResponse(True,safe=False)

def feedback(request,meeting):
    if request.user.is_authenticated:
        doctor = False
    else:
        doctor = True
    return render(request,"feedback.html",{"prescription_slug":meeting,"doctor":doctor})

def feedback_submit(request):
    prescription = request.GET.get("prescription")
    prescription = Prescription.objects.get(slug=prescription)
    rating = request.GET.get("rating")
    comments = request.GET.get("comments")
    feedbacks = Feedback.objects.filter(prescription=prescription)
    if len(feedbacks) > 0:
        feedback = feedbacks.last()
        if request.user.is_authenticated:
            feedback.patient_rating=rating
            feedback.patient_comments=comments
        else:
            feedback.doctor_rating=rating
            feedback.doctor_comments=comments
    else:
        if request.GET.get("patient"):
            feedback = Feedback(prescription=prescription,patient_rating=rating,patient_comments=comments)
        else:
            feedback = Feedback(prescription=prescription,doctor_rating=rating,doctor_comments=comments)
    feedback.save()
    return JsonResponse(True,safe=False)


def statistics(request):
    users = len(Customer.objects.all())
    doctors = len(Doctor.objects.all())
    appointments = len(Appointments.objects.all())
    data = {"users":users,"doctors":doctors,"appointments":appointments}
    return JsonResponse(data,safe=False)

def index(request):
    all_links = Links.objects.all()
    feedbacks = Feedback.objects.filter(Q(status_doctor=True) | Q(status_patient=True))
    return render(request,"index/index.html",{"links":all_links,"doctor_types":doctor_types,"paramedic_types":paramedic_types,"feedbacks":feedbacks})


def email_contact_form(request):

    name = request.GET.get("name")
    email = request.GET.get("email").strip()
    phone = request.GET.get("phone")
    message = request.GET.get("message")
    body ="Name : "+name+"\nEmail : "+email+"\n Phone : "+phone+"\nMessage : "+message
    email_msg = EmailMessage("pdochealth consultancy enquiry", body, settings.EMAIL_HOST_USER, ["care@pdochealth.com"])
    email_msg.send(fail_silently=False)
    return JsonResponse(True,safe=False)

