from django.db import models
from django.contrib.auth.models import User

class Warehouse(models.Model):
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class JobTitle(models.Model):
    name = models.CharField(max_length=200)
    code = models.IntegerField(default=0)
    issue_rate_notes = models.TextField(default='')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

class Department(models.Model):
    name = models.CharField(max_length=200)
    boss = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=200, default='', help_text = 'Имя')
    surname = models.CharField(max_length=200, default='', help_text = 'Фамилия')
    patronymic = models.CharField(max_length=200, default='', help_text = 'Отчество')
    personnel_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    sex = models.CharField(max_length=20)
    size_of_clothes = models.FloatField(default=0)
    size_of_boots = models.FloatField(default=0)
    size_of_head = models.FloatField(default=0)
    size_of_hand = models.FloatField(default=0)
    employment_start_date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} {self.name} {self.patronymic}'

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class SIZ(models.Model):
    name = models.CharField(max_length=200, default='')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    code = models.IntegerField(default=0)
    clothes_type = models.CharField(
        max_length=200, 
        null=True,
        choices = [
            ('Руки', 'Руки'),
            ('Ноги', 'Ноги'),
            ('Общий', 'Общий'),
            ('Голова', 'Голова')
        ]
    )
    clothes_size = models.FloatField(default=0)
    issued_siz = models.ManyToManyField(Worker, through='IssuedItem')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'СИЗ'
        verbose_name_plural = 'СИЗы'

class IssuedItem(models.Model):
    issued_date = models.DateTimeField(null=True)
    expired_date = models.DateTimeField(null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    siz = models.ForeignKey(SIZ, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Выделенная вещь'
        verbose_name_plural = 'Выделенные вещи'


class SIZOrder(models.Model):
    date = models.DateTimeField()
    required_siz = models.ForeignKey(SIZ, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:        
        verbose_name = 'Заказ СИЗ'
        verbose_name_plural = 'Заказы СИЗ'
