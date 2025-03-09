from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class ExpenseType(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Expense(models.Model):
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT)
    amount = models.FloatField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    purchased_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type.name} - {self.source.name} - {datetime.strftime(self.purchased_date, '%d %b, %y')}"


class IncomeType(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Income(models.Model):
    income_type = models.ForeignKey(IncomeType, on_delete=models.PROTECT)
    amount = models.FloatField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    received_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
