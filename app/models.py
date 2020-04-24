from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

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

class Doctor(User):

    name = models.CharField(max_length=200)
    address = models.TextField()
    education = models.TextField()
    practicing_year = models.CharField(max_length=100)
    image = models.ImageField(upload_to="doctors/")
    gender = models.CharField(max_length=100)
    description = models.TextField()
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

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
    direct_contact = models.BooleanField(default=True)

    def __str__(self):
        return self.name
