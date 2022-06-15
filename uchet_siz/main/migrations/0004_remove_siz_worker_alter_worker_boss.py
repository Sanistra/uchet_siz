# Generated by Django 4.0.5 on 2022-06-07 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_worker_boss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siz',
            name='worker',
        ),
        migrations.AlterField(
            model_name='worker',
            name='boss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.worker'),
        ),
    ]
