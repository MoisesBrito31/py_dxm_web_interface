from django.urls import path
from .views import IndexView, LinhaView, HistoricoView, ConjuntoView, GraficoVView
from .views import conjunto_linhas, get_linha, set_vel_esp, set_forma, get_v_aovivo
from .views import set_t_p_prog, relatorio

urlpatterns = [
    path('index/<int:valor>', IndexView.as_view(), name='oee_index'),
    path('linha/<int:id>',LinhaView.as_view(), name='linha'),
    path('historico/<int:valor>',HistoricoView.as_view(), name='historico'),
    path('grafico_v/<int:id>',GraficoVView.as_view(), name='grafico_v'),
    path('conjunto_linhas/', conjunto_linhas, name='conjunto_linhas'),
    path('overview', ConjuntoView.as_view(), name='overview'),
    path('set_vel_esp/<int:index>/<int:valor>', set_vel_esp, name='set_vel_esp'),
    path('set_forma/<int:index>/<int:valor>', set_forma, name='set_forma'),
    path('set_t_p_prog/<int:index>/<int:valor>', set_t_p_prog, name='set_t_p_prog'),
    path('relatorio/<str:inis>/<str:fims>/<int:valor>', relatorio, name='relatorio'),
    path('get_linha/<int:id>', get_linha, name='get_linha'),
    path('get_v_aovivo/<int:id>', get_v_aovivo, name='get_v_aovivo')
]
