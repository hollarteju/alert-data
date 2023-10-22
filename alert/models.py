from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import  BaseUserManager
from django.utils import timezone



# Create your models here.

class UserDataManager(BaseUserManager):
    def create_user(self, username, password=None, **others):
        if not username:
            raise ValueError("incorrect email")
        if not password:
            raise ValueError("incorrect .py runserverpassword")
        # email = self.normalize_email(email)
        user = self.model(username=username, **others)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, password=None):
        if not username:
            raise ValueError("wrong email")
        if not password:
            raise ValueError("wrong password")
        user = self.create_user(username, password)
   
        user.is_staff = True
        user.is_superuser = True

        user.save()
        return user


class UserData(AbstractBaseUser,PermissionsMixin):
    # images_data = models.ManyToManyField("self", through="image")
    email = models.EmailField(max_length=100, blank=True)
    username = models.CharField(max_length= 50, unique=True)
    password = models.CharField(max_length=228)
    confirm_password = models.CharField(max_length=228, blank=True)
    phone_number = models.CharField(max_length=15,blank=True)
    state = models.TextField(max_length= 20,blank=True)
    city = models.TextField(max_length= 20,blank=True)
    district = models.TextField(max_length= 20,blank=True)
    is_superuser = models.BooleanField(default= True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
   
    USERNAME_FIELD= "username"

    REQUIRED_FIELDS= [
        
                      "password"
                     
                      ]
    objects = UserDataManager()
   
   
def password_validate(clean_data):
    try:
        assert clean_data["password"] == clean_data["confirm_password"]
       
    except AssertionError:
        print("password needs to be same")   
      

class ProfilePicture(models.Model):
    user = models.OneToOneField(UserData, on_delete=models.CASCADE, related_name="image_field")
    image  = models.FileField(upload_to="images", blank=True)
    avatar  = models.FileField(upload_to="avatars", blank=True)

    def __str__(self):
        return self.user.username
    
class Timeline(models.Model):
    user = models.ForeignKey(UserData, on_delete= models.CASCADE, related_name= "time_line")
    timeline_message = models.TextField(max_length=1000000, blank=True)
    timeline_media= models.FileField(upload_to="timeline", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

  
    
class Reaction(models.Model):
    REACTION_CHOICES= [("Like","like"), ("Dislike","dislike"),("Witness","witness")]

    user = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name="reations")
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)



        