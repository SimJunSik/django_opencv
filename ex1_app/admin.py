from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Dog)
admin.site.register(TestModel)
admin.site.register(Version)
admin.site.register(Thumbnail)
admin.site.register(Client)
admin.site.register(FriendList)
admin.site.register(FriendAddList)