from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('propertyname/', views.propertyname.as_view()),
    path('propertylocation/', views.propertylocation.as_view()),
    path('api/bin/', views.bin_list),
    path('api/scan/', views.scan_list),
    path('api/collection_task/', views.collection_task_list),
    # path('api/scan_detail/<int:pk>/', views.)
]