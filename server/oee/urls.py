from django.urls import path
from .views import IndexView, LinhaView
from .views import conjunto_linhas, get_linha, set_vel_esp, set_forma,set_t_p_prog

urlpatterns = [
    path('', IndexView.as_view(), name='oee_index'),
    path('linha/<int:id>',LinhaView.as_view(), name='linha'),
    path('conjunto_linhas', conjunto_linhas, name='conjunto_linhas'),
    path('set_vel_esp/<int:index>/<int:valor>', set_vel_esp, name='set_vel_esp'),
    path('set_forma/<int:index>/<int:valor>', set_forma, name='set_forma'),
    path('set_t_p_prog/<int:index>/<int:valor>', set_t_p_prog, name='set_t_p_prog'),
    path('get_linha/<int:id>', get_linha, name='get_linha')
]
