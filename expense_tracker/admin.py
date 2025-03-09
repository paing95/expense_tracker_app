from django.contrib import admin
from django.contrib.auth.models import User
from import_export.admin import ExportActionModelAdmin
from rangefilter.filters import DateRangeFilterBuilder

from .models import Income, IncomeType
from .models import Expense, ExpenseType
from .models import Source


@admin.register(IncomeType)
class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "user"):
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Income)
class IncomeAdmin(ExportActionModelAdmin):
    list_display = (
        "received_date",
        "income_type__name",
        "source__name",
        "amount",
    )
    ordering = (
        "-received_date",
        "income_type__name",
    )
    fields = (
        "income_type",
        "amount",
        "source",
        "description",
        "received_date",
    )
    list_filter = (("received_date", DateRangeFilterBuilder()),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "source":
            kwargs["queryset"] = Source.objects.order_by("name")
        if db_field.name == "income_type":
            kwargs["queryset"] = IncomeType.objects.order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "user"):
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Expense)
class ExpenseAdmin(ExportActionModelAdmin):
    list_display = (
        "purchased_date",
        "expense_type__name",
        "source__name",
        "amount",
    )
    ordering = (
        "-purchased_date",
        "expense_type__name",
    )
    fields = (
        "expense_type",
        "amount",
        "source",
        "description",
        "purchased_date",
    )
    list_filter = (("purchased_date", DateRangeFilterBuilder()),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "source":
            kwargs["queryset"] = Source.objects.order_by("name")
        if db_field.name == "expense_type":
            kwargs["queryset"] = ExpenseType.objects.order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    ordering = ("name",)
    fields = ("name",)

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "user"):
            obj.user = request.user
        super().save_model(request, obj, form, change)
