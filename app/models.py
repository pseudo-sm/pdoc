from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from tinymce.models import HTMLField
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.BooleanField(default=False)
    type_category = models.CharField(max_length=3)
    image = models.ImageField(upload_to="types/",default="types/default.png")
    def __str__(self):
        return self.name

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    practice_id = models.CharField(max_length=100,default="null")
    name = models.CharField(max_length=200)
    address = models.TextField()
    education = models.TextField()
    practicing_year = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to="doctors/",null=True,blank=True)
    gender = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    lat = models.CharField(max_length=100,null=True,blank=True)
    lon = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    videoconferencing = models.BooleanField(default=False)
    telecalling = models.BooleanField(default=False)
    available_from = models.TimeField()
    available_to = models.TimeField()
    signuptime = models.DateTimeField(auto_now=True)
    direct_contact = models.BooleanField(default=False)
    designation = models.CharField(max_length=300,null=True,blank=True)
    hospital = models.CharField(max_length=300)
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    @property
    def get_experience(self):
        return self.practicing_year

    def __str__(self):
        return self.name

class TeleCallDoctors(models.Model):

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20,null=True,blank=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    education = models.CharField(max_length=200,null=True,blank=True)
    practicing_year = models.CharField(max_length=20,null=True,blank=True)
    designation = models.CharField(max_length=200,null=True,blank=True)
    hospital = models.CharField(max_length=200,null=True,blank=True)
    registration_id = models.CharField(max_length=200,null=True,blank=True)
    available_from = models.CharField(max_length=200,null=True,blank=True)
    available_to = models.CharField(max_length=200,null=True,blank=True)
    direct_contact = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    address = models.TextField(null=True,blank=True)
    #doctors who want to register with
    def __str__(self):
        return self.name

class Links(models.Model):

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Customer(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    query = models.TextField()
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    razor_pay_order_id = models.CharField(max_length=1000,null=True,blank=True)
    datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Paramedics(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=20)
    available_from = models.CharField(max_length=200,null=True,blank=True)
    available_to = models.CharField(max_length=200,null=True,blank=True)
    achievements = models.CharField(max_length=200,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    designation = models.CharField(max_length=200,null=True,blank=True)
    organization = models.CharField(max_length=200,null=True,blank=True)
    license_no = models.CharField(max_length=100,unique=True,null=True,blank=True)
    collection = models.BooleanField(null=True,blank=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " ("+str(self.type)+")"



class Others(models.Model):

    name = models.CharField(max_length=100)
    value = HTMLField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=300)
    article = HTMLField()
    slug = models.SlugField()
    datetime = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to="articles",null=True,blank=True)

    def __str__(self):
        return self.title

class Appointments(models.Model):

    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=200,blank=True,null=True)
    query = models.TextField()
    type = models.CharField(max_length=3)
    datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,default=0)
    time = models.DateTimeField(null=True,blank=True)
    slug = models.SlugField(auto_created=True)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    count = models.CharField(max_length=10,default=0)
    def __str__(self):
        return str(self.id)

class ParamedicBookings(models.Model):

    id = models.AutoField(primary_key=True)
    paramedic = models.ForeignKey(Paramedics,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=200,blank=True,null=True)
    query = models.TextField()
    type = models.CharField(max_length=3)
    datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,default=0)
    def __str__(self):
        return str(self.id)


class Prescription(models.Model):

    appointment = models.ForeignKey(Appointments,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    medicine = models.CharField(max_length=300)
    morning = models.BooleanField(max_length=10)
    lunch = models.BooleanField(max_length=10)
    evening = models.BooleanField(max_length=10)
    dinner = models.BooleanField(max_length=10)
    afterFood = models.BooleanField(max_length=300)
    period = models.CharField(max_length=300)
    quantity = models.CharField(max_length=300)
    remarks = models.TextField()
    summary = models.TextField()

class Terms(models.Model):
    id = models.AutoField(primary_key=True)
    terms = HTMLField()
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.datetime)
