from django.urls import path
from .views import online, IndexView, TurnosView
from .views import Set_ip, Set_linhas, Set_tickLog, emula, zerarLinha, Set_dados
from .views import AddTurno, DeleteTurno, EditTurno
from .views import getRelogio, setRelogio

urlpatterns = [
    path('', IndexView.as_view(), name='config'),
    path('turno', TurnosView.as_view(), name='turno'),
    path('addTurno', AddTurno.as_view(), name='add_turno'),
    path('deletaTurno/<int:value>', DeleteTurno.as_view(), name='deleta_turno'),
    path('editTurno/<int:value>', EditTurno.as_view(), name='edit_turno'),
    path('getRelogio',getRelogio, name='get_relogio'),
    path('setRelogio',setRelogio, name='set_relogio'),
    path('set_ip', Set_ip.as_view(), name='set_ip'),
    path('set_linhas', Set_linhas.as_view(), name='set_linhas'),
    path('set_tickLog', Set_tickLog.as_view(), name='set_tickLog'),
    path('emula/<int:valor>', emula, name='emula'),
    path('zerar_linha/<int:valor>',zerarLinha, name='zerar_linha'),
    path('set_dados/<int:valor>', Set_dados.as_view(), name='set_dados'),
    path('online', online, name='online'),
]