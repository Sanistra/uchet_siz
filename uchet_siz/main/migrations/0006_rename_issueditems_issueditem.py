# Generated by Django 4.0.5 on 2022-06-07 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_siz_wearing_type_alter_siz_clothes_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IssuedItems',
            new_name='IssuedItem',
        ),
    ]
