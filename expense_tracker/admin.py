from django.contrib import admin

from .models import Income, IncomeType
from .models import Expense, ExpenseType
from .models import Source

@admin.register(IncomeType)
class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('received_date', 'income_type__name', 'source__name', 'amount',)
    ordering = ('-received_date', 'income_type__name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'source':
            kwargs['queryset'] = Source.objects.order_by('name')
        if db_field.name == 'income_type':
            kwargs['queryset'] = IncomeType.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('purchased_date', 'expense_type__name', 'source__name', 'amount',)
    ordering = ('-purchased_date', 'expense_type__name',)
    fields = ('expense_type', 'amount', 'source', 'description', 'purchased_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'source':
            kwargs['queryset'] = Source.objects.order_by('name')
        if db_field.name == 'expense_type':
            kwargs['queryset'] = ExpenseType.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    ordering = ('name',)