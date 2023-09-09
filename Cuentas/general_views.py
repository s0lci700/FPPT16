from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import pytz
import locale
from Fichas.models import Assignment

chile = pytz.timezone("America/Santiago")
chile_time = datetime.now(chile)

# General views


def landing_view(request):
    return render(request, "landing.html")


@login_required
def home_view(request):
    assignments = Assignment.objects.all()
    current_datetime = timezone.now()

    # Count of open, non-filled fichas by user
    open_non_filled_fichas = (
        Assignment.objects.filter(
            time_window_start__lte=current_datetime,
            time_window_end__gte=current_datetime,
        )
        .exclude(fichas__student__user=request.user)
        .count()
    )
    # Find the assignment with the closest end time that's still open and not filled by the user
    closest_assignment = (
        Assignment.objects.filter(time_window_end__gte=current_datetime)  # Still open
        .exclude(fichas__student__user=request.user)  # Not yet filled by the user
        .order_by("time_window_end")  # Order by end time
        .first()
    )  # Take the first one, which will be the closest

    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Set locale to Spanish
    weekday = chile_time.strftime("%A")  # Gives day of the week
    day_number = chile_time.day  # Gives the day number
    month = chile_time.strftime("%B")  # Gives the month
    year = chile_time.year  # Gives the year

    context = {
        "current_datetime": current_datetime,
        "assignments": assignments,
        "weekday": weekday,
        "day_number": day_number,
        "month": month,
        "year": year,
        "open_non_filled_fichas": open_non_filled_fichas,
        "closest_assignment": closest_assignment,  # Add this line
    }

    return render(request, "home.html", context)
