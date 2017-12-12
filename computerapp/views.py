from django.shortcuts import render

# Create your views here.

from rest_framework import generics,permissions
from computerapp.models import Product,UserProfile
from computerapp.serializers import ProductListSerializer,\
ProductRetrieveSerializer,UserInfoSerializer,UserProfileSerializer
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductListView(generics.ListAPIView):

	queryset = Product.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = (permissions.AllowAny,)
	filter_backends = (OrderingFilter,SearchFilter,)
	ordering_fields = ('category','manufacturer','created','sold',)
	search_fields = ('description','model',)
	ordering = ('id',)
	pagination_class = LimitOffsetPagination

class ProductListByCategoryView(generics.ListAPIView):
	serializer_class = ProductListSerializer
	permission_classes = (permissions.AllowAny,)
	filter_backends = (SearchFilter,OrderingFilter,)
	search_fields = ('description',)
	ordering_fields = ('category','manufacturer','created','sold','price')
	ordering = ('id',)

	def get_queryset(self):
		category = self.request.query_params.get('category',None)
		if category is not None:
			queryset = Product.objects.filter(category=category)
		else:
			queryset = Product.objects.all()
		return queryset

class ProductListByCategoryManufacturerView(generics.ListAPIView):
	'''
	产品按类别按品牌列表
	'''
	serializer_class = ProductListSerializer
	permission_classes = (permissions.AllowAny,)
	filter_backends = (SearchFilter,OrderingFilter,)
	search_fields = ('description',)
	ordering_fields = ('category','manufacturer','created','sold','price')
	ordering = ('id',)
	def get_queryset(self):
		category = self.request.query_params.get('category',None)
		manufacturer = self.request.query_params.get('manufacturer',None)
		if category is not None:
			queryset = Product.objects.filter(category=category,
				manufacturer=manufacturer)
		else:
			queryset = Product.objects.all()
		return queryset


class ProductRetrieveView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductRetrieveSerializer
	permission_classes = (permissions.AllowAny,)

class UserInfoView(APIView):
	'''
	用户基本信息
	'''
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request,format=None):
		user = self.request.user
		serializer = UserInfoSerializer(user)
		return Response(serializer.data)

class UserProfileRUView(generics.RetrieveUpdateAPIView):
	'''
	用户其他信息
	'''
	serializer_class = UserProfileSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_object(self):
	
		user = self.request.user
	
		obj = UserProfile.objects.get(user=user)
	
		return obj