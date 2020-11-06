from django.urls import path
from .views import IndexView, conjunto_linhas

urlpatterns = [
    path('', IndexView.as_view(), name='oee_index'),
    path('conjunto_linhas', conjunto_linhas, name='conjunto_linhas')
]
