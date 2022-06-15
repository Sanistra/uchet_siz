from django.contrib import admin
from django.db.models.functions import Lower
import csv
from django.http import HttpResponse

from .models import *


class SIZInline(admin.TabularInline):
    model = SIZ


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = [SIZInline]


@admin.register(SIZ)
class SIZAdmin(admin.ModelAdmin):
    list_display = ('name', 'clothes_size', 'quantity', 'lifespan')
    search_fields = ('name', 'clothes_type', 'clothes_size')

    def get_ordering(self, request):
        return [Lower('name')]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'boss')


@admin.register(IssuableItem)
class IssuableItemAdmin(admin.ModelAdmin):
    list_display = ('siz', 'quantity', 'job_title')


class IssuableItemInline(admin.TabularInline):
    model = SIZ.issuable_siz.through


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    inlines = [IssuableItemInline]


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
    pass


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
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Выгрузить заказы в формате CSV"
