from django.urls import path
from .views import online, IndexView, TurnosView, MapIoView, DxmConfigView
from .views import Set_ip, Set_linhas, Set_tickLog, emula, zerarLinha, Set_dados
from .views import AddTurno, DeleteTurno, EditTurno, MapAltModo
from .views import getRelogio, setRelogio
from .views import destravar, travar, sendXml, sendScript, fileExist, fileDelete, fileDownload

urlpatterns = [
    path('', IndexView.as_view(), name='config'),
    path('turno', TurnosView.as_view(), name='turno'),
    path('mapio', MapIoView.as_view(), name='map_io'),
    path('dxmconfig', DxmConfigView.as_view(), name='dxm_config'),
    path('mapaltmodo', MapAltModo.as_view(), name='map_alt_modo'),
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
    path('travar',travar,name='travar'),
    path('destravar', destravar, name='destravar'),
    path('sendxml', sendXml, name='send_xml'),
    path('sendscript',sendScript,name='send_script'),
    path('fileexist/<str:file>',fileExist, name='file_exist'),
    path('filedelete/<str:file>',fileDelete, name='file_delete'),
    path('fileget/<str:file>',fileDownload, name='file_get'),
    path('online', online, name='online'),
]