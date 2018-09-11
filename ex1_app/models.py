import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

class Dog(models.Model) :
	
	name=models.CharField(max_length=50,default="unknown")


class Version(models.Model):
    version = models.CharField(max_length=10)
    osType = models.CharField(max_length=10, default='android')
 
    def __str__(self):
        return self.version


class User(models.Model):
    user_id = models.CharField(max_length=20)
    user_psw = models.CharField(max_length=20)
 
    def __str__(self):
        return self.user_id

class Thumbnail(models.Model) :
    thumbnail_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, default='none')
    #thumbnail_id = models.IntegerField(primary_key=True, default = 1)
    bytes_list = models.TextField('DESCRIPTION')
    img = models.ImageField(default='./my.png', upload_to='')
    video = models.FileField(default='', upload_to='')
    def __str__(self):
        return str(self.thumbnail_id)


class TestModel(models.Model) :
	Name = models.CharField(max_length=10)
	def __str__(self) :
		return self.Name


class Photo(models.Model):
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'



class Client(models.Model):

    #clientid = models.CharField(max_length=50, primary_key=True)
    clientid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.clientid

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class PassId(models.Model):
    passid = models.CharField(max_length=50)

    def __str__(self):
        return self.passid

class Media(models.Model):


    #clientid = models.ForeignKey(Client, on_delete=models.CASCADE, default="1")
    clientid = models.CharField(max_length=50, default = "1")
    img = models.ImageField(upload_to='img/', default='')
    video = models.FileField(upload_to='video/', default='')

      #def __init__(self, img, video):
   #   self.img = img
   #   self.author = author

   #def __str__(self):
   #   return "__str__"


    def __str__(self):
        return self.clientid


class FriendList(models.Model):

    clientid = models.CharField(max_length=50)
    friendid = models.CharField(max_length=50)

    def __str__(self):
        return self.clientid

class FriendAddList(models.Model):

    clientid = models.CharField(max_length=50)
    friendid = models.CharField(max_length=50)

    def __str__(self):
        return self.clientid