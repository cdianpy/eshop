from rest_framework import serializers
from computerapp.models import Product,Manufacturer,Category,UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('id','user','mobile_phone','nickname',
			'description','icon','created','updated')
		read_only_fields = ('user',) 


class UserInfoSerializer(serializers.ModelSerializer):
	profile_of = UserProfileSerializer()
	class Meta:
		model = User
		fields = ('id','username','email','first_name',
			'last_name','date_joined','profile_of') 

class ManufacturerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Manufacturer
		fields = ('id','name',)

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id','name',)

class ProductListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ('id','model','image','price','sold','category',
			'manufacturer')


class ProductRetrieveSerializer(serializers.ModelSerializer):
	manufacturer = ManufacturerSerializer()
	category = CategorySerializer()
	class Meta:
		model = Product
		fields = ('id','model','image','price','sold','category',
			'manufacturer','description','created','updated')


