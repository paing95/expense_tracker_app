from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .data import (
    get_monthly_expense_by_type,
    get_monthly_income_by_type,
    get_monthly_summary,
)
from .data import get_monthly_expense_details, get_monthly_income_details
from .forms import LoginForm

from datetime import datetime
from dateutil.relativedelta import *


def LoginView(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.error(request, "Wrong login credentials.")
                return render(request, "login.html", {"form": form})
            login(request, user)
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("login")


def DashboardView(request):
    if not request.user.is_authenticated:
        return redirect("/")

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_date = datetime.now() + relativedelta(day=1)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end_date = (
            datetime.now()
            + relativedelta(day=1)
            + relativedelta(months=+1)
            + relativedelta(days=-1)
        )

    return render(
        request,
        "dashboard.html",
        {
            "monthly_expense": list(
                get_monthly_expense_by_type(start_date.date(), end_date.date())
            ),
            "monthly_income": list(
                get_monthly_income_by_type(start_date.date(), end_date.date())
            ),
            "summary": get_monthly_summary(start_date.date(), end_date.date()),
            "monthly_expense_source": get_monthly_expense_details(
                start_date.date(), end_date.date()
            ),
            "monthly_income_source": get_monthly_income_details(
                start_date.date(), end_date.date()
            ),
        },
    )
