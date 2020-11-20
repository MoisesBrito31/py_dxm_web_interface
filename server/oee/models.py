from django.db import models


class Hist(models.Model):
    linha = models.IntegerField('linha')
    time = models.DateTimeField('time')
    oee = models.IntegerField('oee')
    dis = models.IntegerField('dis')
    q = models.IntegerField('q')
    per = models.IntegerField('per')
    vel_atu = models.IntegerField('vel_esp')
    bons = models.IntegerField('bons')
    ruins_total = models.IntegerField('ruins_total')
    t_par = models.IntegerField('t_par')
    t_prod = models.IntegerField('t_prod')

    class Meta:
        verbose_name = 'Historico'
        verbose_name_plural = 'Historicos'        

    def __str__(self):
        return str(self.linha)