from django.contrib import admin
import csv

from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path

from .models import *


class SIZInline(admin.TabularInline):
    model = SIZ


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = [SIZInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'boss')


@admin.register(SIZ)
class SIZAdmin(admin.ModelAdmin):
    list_display = ('name', 'clothes_size', 'quantity', 'lifespan')
    search_fields = ('name', 'clothes_type', 'clothes_size')

    def get_ordering(self, request):
        return [Lower('name')]


class IssuableItemInline(admin.TabularInline):
    model = SIZ.issuable_siz.through


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    inlines = [IssuableItemInline]


@admin.register(IssuableItem)
class IssuableItemAdmin(admin.ModelAdmin):
    list_display = ('siz', 'quantity', 'job_title')


class IssuedItemInline(admin.TabularInline):
    model = SIZ.issued_siz.through
    fields = ('siz', 'issue_reason', 'issued', 'quantity', 'issued_date', 'expired_date')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('fio', 'department', 'job_title')
    search_fields = ('name', 'surname', 'patronymic', 'department__name', 'job_title__name')

    inlines = [IssuedItemInline]


@admin.register(SIZOrder)
class SIZOrderAdmin(admin.ModelAdmin):
    change_list_template = "main/siz_order_changelist.html"
    list_display = ('date', 'required_siz', 'quantity')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('make_order/', self.make_order),
        ]
        return my_urls + urls

    def make_order(self, request):
        expired_siz = IssuedItem.objects.filter(
            Q(expired_date__lte=datetime.datetime.now() + datetime.timedelta(days=30))
            | Q(issued=IssuedItem.ISSUED_STATUS_EXPIRED)
        )

        SIZOrder.objects.all().delete()

        to_order_siz = []

        for siz in expired_siz:
            to_order_siz.append(
                SIZOrder(
                    date=datetime.date.today(),
                    required_siz=siz.siz,
                    quantity=siz.quantity
                )
            )

        SIZOrder.objects.bulk_create(to_order_siz)

        return HttpResponseRedirect("../")

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = []

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        for obj in queryset:
            row = {
                "Название": obj.required_siz.name,
                "Тип": obj.required_siz.clothes_type,
                "Размер": obj.required_siz.clothes_size,
                "Количество": obj.quantity,
            }

            if not field_names:
                field_names = row.keys()
                writer.writerow(field_names)

            writer.writerow(row.values())

        return response

    export_as_csv.short_description = "Выгрузить заказы в формате CSV"



@admin.register(IssuedItem)
class IssuedItemAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Выгрузить заказы в формате CSV"
