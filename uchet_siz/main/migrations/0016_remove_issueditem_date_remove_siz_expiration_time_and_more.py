# Generated by Django 4.0.5 on 2022-06-07 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_siz_issued_siz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issueditem',
            name='date',
        ),
        migrations.RemoveField(
            model_name='siz',
            name='expiration_time',
        ),
        migrations.AddField(
            model_name='issueditem',
            name='expired_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='issueditem',
            name='issued_date',
            field=models.DateTimeField(null=True),
        ),
    ]
