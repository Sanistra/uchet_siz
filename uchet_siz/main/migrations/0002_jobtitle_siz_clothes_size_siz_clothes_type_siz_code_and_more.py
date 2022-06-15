# Generated by Django 4.0.5 on 2022-06-07 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='siz',
            name='clothes_size',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='siz',
            name='clothes_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='siz',
            name='code',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='siz',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='siz',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.warehouse'),
        ),
        migrations.AddField(
            model_name='siz',
            name='wearing_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personnel_number', models.IntegerField()),
                ('department', models.CharField(max_length=200)),
                ('sex', models.CharField(max_length=20)),
                ('size_of_clothes', models.FloatField(default=0)),
                ('size_of_boots', models.FloatField(default=0)),
                ('size_of_head', models.FloatField(default=0)),
                ('size_of_hand', models.FloatField(default=0)),
                ('employment_start_date', models.DateTimeField()),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.jobtitle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('siz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.siz')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.worker')),
            ],
        ),
        migrations.AddField(
            model_name='siz',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.worker'),
        ),
    ]
