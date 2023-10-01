from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

# Create your models here.

class UserManagerModel(BaseUserManager):
    def create_user(self , first_name , last_name , email , username , password=None ):
        if not email :
            raise ValueError("user must have email addres !")
        if not username :
            raise ValueError("user must have a username !")

        user = self.model(
            email=self.normalize_email(email),
            username = username ,
            first_name = first_name ,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self , first_name , last_name , email , username , password = None ):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username ,
            password=password,
            first_name = first_name ,
            last_name = last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff= True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (VENDOR , 'vendor'),
        (CUSTOMER , 'customer')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(unique=True)
    role= models.PositiveSmallIntegerField(choices=ROLE_CHOICE ,blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']

    objects = UserManagerModel()

    def __str__(self):
        return f"{self.username} , {self.email}"
    
    def has_perm(self ,perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True
    
    def get_role(self):
        if self.role == 1 :
            return "vendor"
        else :
            return "customer"
        
class UserProfileModel(models.Model):
    user = models.OneToOneField(UserModel , on_delete=models.CASCADE ,blank=True , null=True)
    profile_picture =models.ImageField(upload_to='users/profile_pictures' , blank=True , null=True)
    cover_picture =models.ImageField(upload_to='users/cover_pictures' , blank=True , null=True)
    address= models.CharField(max_length=250 , blank=True , null=True )
    country = models.CharField(max_length=30 , blank=True , null=True)
    state = models.CharField(max_length=30 , blank=True , null=True)
    city = models.CharField(max_length=30 , blank=True , null=True)
    latitude=models.CharField(max_length=10 , blank=True , null=True)
    longitude = models.CharField(max_length=10 , blank=True , null=True)
    location = gismodels.PointField(blank=True , null=True , srid=4326)
    creat_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}"
    
    def save(self , *args, **kwargs):
        if self.latitude and self.longitude :
            #first we should ad  long then add lat here
            self.location = Point(float(self.longitude ), float(self.latitude) ) #long and lat muset be float
            return super(UserProfileModel , self).save(*args, **kwargs)
        return super(UserProfileModel , self).save(*args, **kwargs)

        