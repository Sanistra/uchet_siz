from django.db import models
from django.contrib.auth.models import User


class Warehouse(models.Model):
    address = models.CharField(max_length=200, verbose_name='Адрес')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class JobTitle(models.Model):
    name = models.CharField(max_length=200, verbose_name='Должность')
    code = models.IntegerField(default=0, verbose_name='Код должности')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название отдела')
    boss = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Начальник отдела')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='Имя')
    surname = models.CharField(max_length=200, default='', verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, default='', verbose_name='Отчество')
    personnel_number = models.IntegerField(verbose_name='Табельный номер')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учетная запись')
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, verbose_name='Должность')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отдел')
    sex = models.CharField(max_length=20, verbose_name='Пол')
    size_of_clothes = models.FloatField(default=0, verbose_name='Размер одежды')
    size_of_boots = models.FloatField(default=0, verbose_name='Размер обуви')
    size_of_head = models.FloatField(default=0, verbose_name='Размер головы')
    size_of_hand = models.FloatField(default=0, verbose_name='Размер руки')
    employment_start_date = models.DateTimeField(verbose_name='Дата приема на работу')

    def __str__(self):
        return f'{self.name} {self.name} {self.patronymic}'

    def fio(self):
        return f'{self.surname} {str(self.name)[0]}. {str(self.patronymic)[0]}.'

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class SIZ(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='Название СИЗ')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, verbose_name='Склад')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    code = models.IntegerField(default=0, verbose_name='Код')
    clothes_type = models.CharField(
        max_length=200,
        null=True,
        choices=[
            ('Руки', 'Руки'),
            ('Ноги', 'Ноги'),
            ('Общий', 'Общий'),
            ('Голова', 'Голова'),
            ('Другое', 'Другое'),
        ],
        verbose_name='Тип СИЗ',
    )
    lifespan = models.IntegerField(default=12, verbose_name='Срок эксплуатации (мес.)', null=True, blank=True)
    clothes_size = models.FloatField(default=0, verbose_name='Размер СИЗ', null=True, blank=True)
    issued_siz = models.ManyToManyField(Worker, through='IssuedItem', verbose_name='Выделенный СИЗ')
    issuable_siz = models.ManyToManyField(JobTitle, through='IssuableItem', verbose_name='Выделяемый СИЗ')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'СИЗ'
        verbose_name_plural = 'СИЗы'


class IssuableItem(models.Model):
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.CASCADE,
        verbose_name='Должность',
        null=True,
        blank=True
    )
    siz = models.ForeignKey(SIZ, on_delete=models.CASCADE, verbose_name='СИЗ')
    lifespan = models.IntegerField(default=12, verbose_name='Срок эксплуатации (мес.)')
    quantity = models.IntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f"Выделяемый СИЗ: {self.siz}, для должности: {self.job_title}"

    class Meta:
        verbose_name = 'Выделяемая вещь'
        verbose_name_plural = 'Выделяемые вещи'


class IssuedItem(models.Model):
    issued_date = models.DateTimeField(null=True, verbose_name='Дата выдачи СИЗ')
    expired_date = models.DateTimeField(null=True, verbose_name='Дата истечения срока годности')
    issue_reason = models.CharField(
        max_length=1000,
        null=True,
        default='Другое',
        verbose_name='Причина выдачи'
    )
    issued = models.CharField(
        max_length=200,
        null=True,
        choices=[
            ('Заказано', 'Заказано'),
            ('Выдано', 'Выдано'),
            ('Израсходовано', 'Израсходовано')
        ],
        verbose_name='Статус выданной вещи'
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name='Работник',
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    siz = models.ForeignKey(SIZ, on_delete=models.CASCADE, verbose_name='СИЗ')

    def __str__(self):
        return f"Выделенный СИЗ: {self.siz}, работнику: {self.worker}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Выделенная вещь'
        verbose_name_plural = 'Выделенные вещи'


class SIZOrder(models.Model):
    date = models.DateTimeField(verbose_name='Дата заказа')
    required_siz = models.ForeignKey(SIZ, on_delete=models.CASCADE, null=True, verbose_name='СИЗ')
    quantity = models.IntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.date}: {self.required_siz} - {self.quantity}'

    class Meta:        
        verbose_name = 'Заказ СИЗ'
        verbose_name_plural = 'Заказы СИЗ'
