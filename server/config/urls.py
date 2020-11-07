from django.urls import path
from .views import online

urlpatterns = [
    path('online',online,name='online')
]