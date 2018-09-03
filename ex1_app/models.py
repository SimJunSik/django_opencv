from django.db import models

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
    #thumbnail_id = models.AutoField(primary_key=True, default = 1)
    thumbnail_id = models.IntegerField(primary_key=True, default = 1)
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

