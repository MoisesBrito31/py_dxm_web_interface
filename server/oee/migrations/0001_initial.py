# Generated by Django 3.1 on 2020-11-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linha', models.IntegerField(verbose_name='linha')),
                ('time', models.DateTimeField(verbose_name='time')),
                ('oee', models.IntegerField(verbose_name='oee')),
                ('dis', models.IntegerField(verbose_name='dis')),
                ('q', models.IntegerField(verbose_name='q')),
                ('per', models.IntegerField(verbose_name='per')),
                ('vel_atu', models.IntegerField(verbose_name='vel_esp')),
                ('bons', models.IntegerField(verbose_name='bons')),
                ('ruins_total', models.IntegerField(verbose_name='ruins_total')),
                ('t_par', models.IntegerField(verbose_name='t_par')),
                ('t_prod', models.IntegerField(verbose_name='t_prod')),
            ],
        ),
    ]