# Generated by Django 4.0.5 on 2022-06-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_siz_worker_alter_worker_boss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siz',
            name='wearing_type',
        ),
        migrations.AlterField(
            model_name='siz',
            name='clothes_type',
            field=models.CharField(choices=[('Руки - жесткие перчатки', 'Руки - жесткие перчатки'), ('Руки - мягкие перчатки', 'Руки - мягкие перчатки'), ('Голова - каска', 'Голова - каска'), ('Голова - каска с фонариком', 'Голова - каска с фонариком')], max_length=200, null=True),
        ),
    ]
