from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum, F, Max
from django.shortcuts import render, redirect

from .forms import LoginForm
from .models import Expense, Income

from datetime import datetime
from dateutil.relativedelta import *

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request,
                username=username, password=password
            )
            if not user:
                messages.error(request, 'Wrong login credentials.')
                return render(request, 'login.html', {
                    'form': form
                })
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return redirect('login')


def get_monthly_expense_by_type(startDate, endDate):
    expense_objects_by_amount = Expense.objects \
        .filter(purchased_date__gte=startDate, purchased_date__lte=endDate) \
        .values(expenseTypeName=F('expense_type__name')) \
        .annotate(
            numOfExpense=Count('expense_type'),
            totalExpense=Sum('amount')
        )
    return expense_objects_by_amount


def get_monthly_income_by_type(startDate, endDate):
    income_objects_by_amount = Income.objects \
        .filter(received_date__gte=startDate, received_date__lte=endDate) \
        .values(incomeTypeName=F('income_type__name')) \
        .annotate(
            numOfIncome=Count('income_type'),
            totalIncome=Sum('amount')
        )
    return income_objects_by_amount


def get_monthly_summary(startDate, endDate):
    # Expense
    total_expense = Expense.objects \
        .filter(purchased_date__gte=startDate, purchased_date__lte=endDate) \
        .aggregate(Sum('amount'), Count('id'))
    
    # Expense Count
    max_expense_source_count = 0
    max_expense_source_list = []
    max_expense_source = Expense.objects \
        .filter(purchased_date__gte=startDate, purchased_date__lte=endDate) \
        .values('source') \
        .annotate(
            countOfSource=Count('source')
        ) \
        .order_by('-countOfSource')

    for mes in max_expense_source:
        if mes['countOfSource'] < max_expense_source_count:
            break
        max_expense_source_list.append(mes['source'])
        max_expense_source_count = mes['countOfSource']
    
    # Income
    total_income = Income.objects \
        .filter(received_date__gte=startDate, received_date__lte=endDate) \
        .aggregate(Sum('amount'), Count('id'))

    # Expense Count
    max_income_source_count = 0
    max_income_source_list = []
    max_income_source = Income.objects \
        .filter(received_date__gte=startDate, received_date__lte=endDate) \
        .values('source') \
        .annotate(
            countOfSource=Count('source')
        ) \
        .order_by('-countOfSource')
    
    for mis in max_income_source:
        if mis['countOfSource'] < max_income_source_count:
            break
        max_income_source_list.append(mis['source'])
        max_income_source_count = mis['countOfSource']
    
    return {
        'total_expense': total_expense['amount__sum'],
        'expense_count': total_expense['id__count'],
        'total_income': total_income['amount__sum'],
        'income_count': total_income['id__count'],
        'max_expense': {
            'count': max_expense_source_count,
            'items': max_expense_source_list
        },
        'max_income': {
            'count': max_income_source_count,
            'items': max_income_source_list
        }
    }


def DashboardView(request):
    print(request.GET.get('start_date'), request.GET.get('end_date'))
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = datetime.now() + relativedelta(day=1)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now() + relativedelta(day=1) + relativedelta(months=+1) + relativedelta(days=-1)
    
    return render(request, 'dashboard.html', {
        'monthly_expense': list(get_monthly_expense_by_type(start_date.date(), end_date.date())),
        'monthly_income': list(get_monthly_income_by_type(start_date.date(), end_date.date())),
        'summary': get_monthly_summary(start_date.date(), end_date.date())
    })
