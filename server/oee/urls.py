from django.urls import path
from .views import IndexView, LinhaView, HistoricoView
from .views import conjunto_linhas, get_linha, set_vel_esp, set_forma
from .views import set_t_p_prog, relatorio

urlpatterns = [
    path('', IndexView.as_view(), name='oee_index'),
    path('linha/<int:id>',LinhaView.as_view(), name='linha'),
    path('historico/<int:valor>',HistoricoView.as_view(), name='historico'),
    path('conjunto_linhas', conjunto_linhas, name='conjunto_linhas'),
    path('set_vel_esp/<int:index>/<int:valor>', set_vel_esp, name='set_vel_esp'),
    path('set_forma/<int:index>/<int:valor>', set_forma, name='set_forma'),
    path('set_t_p_prog/<int:index>/<int:valor>', set_t_p_prog, name='set_t_p_prog'),
    path('relatorio/<str:inis>/<str:fims>/<int:valor>', relatorio, name='relatorio'),
    path('get_linha/<int:id>', get_linha, name='get_linha')
]
