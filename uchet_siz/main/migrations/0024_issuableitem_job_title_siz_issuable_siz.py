# Generated by Django 4.0.5 on 2022-06-15 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_issueditem_job_title_issuableitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuableitem',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.jobtitle', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='siz',
            name='issuable_siz',
            field=models.ManyToManyField(through='main.IssuableItem', to='main.jobtitle', verbose_name='Выделяемый СИЗ'),
        ),
    ]