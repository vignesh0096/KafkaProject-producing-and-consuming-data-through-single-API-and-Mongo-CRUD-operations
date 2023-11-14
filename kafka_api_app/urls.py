from django.urls import path
from .views import *

urlpatterns = [
    path('api/', KafkaAPIView.as_view()),
    path('GetData/<str:pk>', GetData.as_view()),
    path('UpdateData/<str:pk>', UpdateData.as_view()),
    path('DeleteData/<str:pk>', DeleteData.as_view()),
]
