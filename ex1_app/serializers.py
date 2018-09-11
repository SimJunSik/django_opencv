from rest_framework import serializers
from .models import *

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id','user_psw')


class ThumbnailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Thumbnail
		fields = ('thumbnail_id','bytes_list','img')



#-*- coding:utf-8 -*-

class TestSerializer(serializers.ModelSerializer):

    

    class Meta:

        model = TestModel

        fields = ('Name',)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:

        model = Client

        fields = ('clientid','password','pub_date',)


class PassIdSerializer(serializers.ModelSerializer):

    class Meta:

        model = PassId

        fields = ('id',)
