from django.urls import path
from .views import online, IndexView, Set_ip
from .views import Set_ip, Set_linhas, Set_tickLog, emula, zerarLinha

urlpatterns = [
    path('', IndexView.as_view(), name='config'),
    path('set_ip', Set_ip.as_view(), name='set_ip'),
    path('set_linhas', Set_linhas.as_view(), name='set_linhas'),
    path('set_tickLog', Set_tickLog.as_view(), name='set_tickLog'),
    path('emula/<int:valor>', emula, name='emula'),
    path('zerar_linha/<int:valor>',zerarLinha, name='zerar_linha'),
    path('online', online, name='online'),
]