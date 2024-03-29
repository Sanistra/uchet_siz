# Generated by Django 4.0.5 on 2022-06-15 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_remove_jobtitle_issue_rate_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issueditem',
            name='job_title',
        ),
        migrations.CreateModel(
            name='IssuableItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lifespan', models.IntegerField(default=12, verbose_name='Срок эксплуатации (мес.)')),
                ('siz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.siz', verbose_name='СИЗ')),
            ],
        ),
    ]
