# Generated by Django 4.0.5 on 2022-06-07 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_jobtitle_issue_rate_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='issued_clothes',
            field=models.ManyToManyField(to='main.siz'),
        ),
        migrations.DeleteModel(
            name='IssuedItem',
        ),
    ]
