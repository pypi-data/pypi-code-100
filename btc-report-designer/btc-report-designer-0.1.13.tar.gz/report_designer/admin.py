from django.contrib import admin

from .models import (
    Report,
    ReportGroup,
    DBTable,
    Format,
    TableField,
    ReportField,
    ReportTable,
)


@admin.register(DBTable)
class DBTableAdmin(admin.ModelAdmin):
    """
    Сущность "Таблица БД" в административной панели
    """

    list_display = (
        'table',
        'alias',
        'is_visible',
    )
    search_fields = ('alias',)
    list_filter = ('is_visible',)
    list_display_links = (
        'table',
        'alias',
    )


@admin.register(ReportGroup)
class ReportGroupAdmin(admin.ModelAdmin):
    """
    Сущность "Группа отчета" в административной панели
    """

    list_display = ('name',)
    search_fields = ('name',)
    list_display_links = list_display


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Сущность "Отчет" в административной панели
    """

    list_display = (
        'name',
        'author',
        'updated',
        'is_visible_in_reports',
    )
    search_fields = ('name',)
    autocomplete_fields = (
        'groups',
        'root',
    )
    list_filter = ('is_visible_in_reports',)
    list_display_links = ('name',)


@admin.register(ReportTable)
class ReportTableAdmin(admin.ModelAdmin):
    """
    Сущность "Отчет" в административной панели
    """

    list_display = (
        'report',
        'db_table',
        'is_root',
    )
    search_fields = ('db_table__name',)
    autocomplete_fields = (
        'report',
        'db_table',
    )
    list_filter = ('is_root',)
    list_display_links = list_display


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    """
    Сущность "Формат" в административной панели
    """

    list_display = (
        'name',
        'internal_type',
    )
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(TableField)
class TableFieldAdmin(admin.ModelAdmin):
    """
    Сущность "Поле таблицы БД" в административной панели
    """

    list_display = (
        'name',
        'alias',
        'db_table',
        'db_field',
        'is_visible',
    )
    search_fields = (
        'name',
        'alias',
    )
    autocomplete_fields = (
        'db_table',
        'representation',
    )
    list_filter = ('is_visible',)
    list_display_links = ('name',)


@admin.register(ReportField)
class ReportFieldAdmin(admin.ModelAdmin):
    """
    Сущность "Поле отчета" в административной панели
    """

    list_display = (
        'name',
        'alias',
        'report',
        'field',
        'order',
    )
    search_fields = (
        'name',
        'alias',
        'report__name',
        'field__name',
    )
    autocomplete_fields = (
        'report',
        'field',
        'representation',
    )
    list_display_links = ('name', 'alias',)
