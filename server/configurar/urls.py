from django.urls import path
from .views import online, IndexView

urlpatterns = [
    path('index', IndexView.as_view(), name='configurar'),
    path('online', online, name='online'),
]