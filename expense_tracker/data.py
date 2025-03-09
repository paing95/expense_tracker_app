from django.db.models import Count, Sum, F, Max
from .models import Expense, Income
from collections import defaultdict


def get_monthly_expense_by_type(startDate, endDate):
    expense_objects_by_amount = (
        Expense.objects.filter(
            purchased_date__gte=startDate, purchased_date__lte=endDate
        )
        .values(expenseTypeName=F("expense_type__name"))
        .annotate(numOfExpense=Count("expense_type"), totalExpense=Sum("amount"))
    )
    return expense_objects_by_amount


def get_monthly_income_by_type(startDate, endDate):
    income_objects_by_amount = (
        Income.objects.filter(received_date__gte=startDate, received_date__lte=endDate)
        .values(incomeTypeName=F("income_type__name"))
        .annotate(numOfIncome=Count("income_type"), totalIncome=Sum("amount"))
    )
    return income_objects_by_amount


def get_monthly_expense_details(startDate, endDate):
    objects = (
        Expense.objects.filter(
            purchased_date__gte=startDate, purchased_date__lte=endDate
        )
        .values("expense_type__name", "source__name", "amount")
        .order_by("expense_type", "source")
    )

    object_dict = {}
    for obj in objects:
        if obj["expense_type__name"] not in object_dict:
            object_dict[obj["expense_type__name"]] = {}

        if obj["source__name"] in object_dict[obj["expense_type__name"]]:
            object_dict[obj["expense_type__name"]][obj["source__name"]] += obj["amount"]
        else:
            object_dict[obj["expense_type__name"]][obj["source__name"]] = obj["amount"]
    return object_dict


def get_monthly_income_details(startDate, endDate):
    objects = (
        Income.objects.filter(received_date__gte=startDate, received_date__lte=endDate)
        .values("income_type__name", "source__name", "amount")
        .order_by("income_type", "source")
    )

    object_dict = {}
    for obj in objects:
        if obj["income_type__name"] not in object_dict:
            object_dict[obj["income_type__name"]] = {}

        if obj["source__name"] in object_dict[obj["income_type__name"]]:
            object_dict[obj["income_type__name"]][obj["source__name"]] += obj["amount"]
        else:
            object_dict[obj["income_type__name"]][obj["source__name"]] = obj["amount"]
    return object_dict


def get_monthly_summary(startDate, endDate):
    # Expense
    total_expense = Expense.objects.filter(
        purchased_date__gte=startDate, purchased_date__lte=endDate
    ).aggregate(Sum("amount"), Count("id"))

    # Expense Count
    max_expense_source_count = 0
    max_expense_source_list = []
    max_expense_source = (
        Expense.objects.filter(
            purchased_date__gte=startDate, purchased_date__lte=endDate
        )
        .values("source")
        .annotate(countOfSource=Count("source"))
        .order_by("-countOfSource")
    )

    for mes in max_expense_source:
        if mes["countOfSource"] < max_expense_source_count:
            break
        max_expense_source_list.append(mes["source"])
        max_expense_source_count = mes["countOfSource"]

    # Income
    total_income = Income.objects.filter(
        received_date__gte=startDate, received_date__lte=endDate
    ).aggregate(Sum("amount"), Count("id"))

    # Expense Count
    max_income_source_count = 0
    max_income_source_list = []
    max_income_source = (
        Income.objects.filter(received_date__gte=startDate, received_date__lte=endDate)
        .values("source")
        .annotate(countOfSource=Count("source"))
        .order_by("-countOfSource")
    )

    for mis in max_income_source:
        if mis["countOfSource"] < max_income_source_count:
            break
        max_income_source_list.append(mis["source"])
        max_income_source_count = mis["countOfSource"]

    return {
        "total_expense": total_expense["amount__sum"],
        "expense_count": total_expense["id__count"],
        "total_income": total_income["amount__sum"],
        "income_count": total_income["id__count"],
        "max_expense": {
            "count": max_expense_source_count,
            "items": max_expense_source_list,
        },
        "max_income": {
            "count": max_income_source_count,
            "items": max_income_source_list,
        },
    }
