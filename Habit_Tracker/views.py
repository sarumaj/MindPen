import calendar
import math
from Journaling.models import Journal
from datetime import datetime


def journaling_frequency(user):

    # get the journals based on the month
    now = datetime.now()
    month = now.month
    year = now.year

    # get journals for the current user and month
    all_journals = Journal.objects.filter(author=user, journal_date__month=month, journal_date__year=year)
    number_journals = all_journals.count()
    total_days_in_month = calendar.monthrange(year, month)[1]

    # frequency of journaling
    journaling_percentage = (number_journals / total_days_in_month) * 100
    return math.floor(journaling_percentage)
