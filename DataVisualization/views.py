from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Endeavors.models import Endeavor
from To_Do.models import Task
from MyMood.models import DataMood
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from .models import PreviousMonth
from django.core.paginator import Paginator


@login_required()
def data(request):

    # get the current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    total = count = 0

    # prepare the data of the current month and displayed
    qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=month)
    dic_data = {
        "Date": [x.mood_date for x in qs],
        "Mood": [int(y.mood_score) for y in qs]
    }

    df = pd.DataFrame(dic_data)
    fig = px.line(
        df,
        x="Date",
        y="Mood",
        title="View of Your Mood",
        labels={"x": "Date", "y": "Mood"},
        markers=True
    )
    fig.update_layout(
        title={
            "font_size": 22,
            "xanchor": "center",
            "x": 0.5,
            "font": {"color": "blue"}
        }
    )
    fig.update_xaxes(
        title="Date",
        tickformat="%d %B <br>%Y",
        showline=True,
        showgrid=True
    )
    chart = fig.to_html()

    # data preparation for pie chart
    crying = sad = angry = disappointed = unhappy = neutral = happy = very_happy = joyful = excited = ecstatic = 0
    for mood in qs:
        if mood.mood_score == "-5":
            crying += 1
        elif mood.mood_score == "-4":
            sad += 1
        elif mood.mood_score == "-3":
            angry += 1
        elif mood.mood_score == "-2":
            disappointed += 1
        elif mood.mood_score == "-1":
            unhappy += 1
        elif mood.mood_score == "0":
            neutral += 1
        elif mood.mood_score == "1":
            happy += 1
        elif mood.mood_score == "2":
            very_happy += 1
        elif mood.mood_score == "3":
            joyful += 1
        elif mood.mood_score == "4":
            excited += 1
        elif mood.mood_score == "5":
            ecstatic += 1
    has_data = any([crying, sad, angry, disappointed, unhappy, neutral, happy, very_happy, joyful, excited, ecstatic])
    if has_data:
        labels = ["crying", "sad", "angry", "disappointed", "unhappy", "neutral", "happy", "very_happy", "joyful", "excited", "ecstatic"]
        values = [crying, sad, angry, disappointed, unhappy, neutral, happy, very_happy, joyful, excited, ecstatic]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    else:
        # create an empty pie chart
        fig = go.Figure(data=[go.Pie(labels=["No Data Yet"], values=[1], hole=.5)])
    pie = fig.to_html()

    # set the variables according to the month
    if month == 1:
        year = year - 1
        previous_month = 12
    else:
        previous_month = month - 1
    # fetch the data oof the previous month
    previous_qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=previous_month)
    # previous exist calculate their average, set new previous instance, and delete that previous queryset.
    if previous_qs:
        for y in previous_qs:
            total += int(y.mood_score)
            count += 1
        average = round(total / count, 2)
        previous = PreviousMonth()
        previous.user = request.user
        previous.average = average
        previous.date = f"{year}-{previous_month:02d}"
        previous.save()
        previous_qs.delete()

    # Progress bar
    all_programs = Endeavor.objects.filter(author=request.user)
    paginator = Paginator(all_programs, 1)  # Show 3 contacts per page.

    progress_data = []

    for program in all_programs:
        all_tasks = Task.objects.filter(endeavor=program)
        tasks = all_tasks.count()
        completed = all_tasks.filter(endeavor=program).filter(completed=True)
        tasks_completed = completed.count()
        remaining_tasks = tasks - tasks_completed

        if tasks == 0:
            progress_percentage = 0
        else:
            progress_percentage = int((tasks_completed / tasks) * 100)

        progress_data.append({"program": program, "progress_percentage": progress_percentage,
                              "remaining_tasks": remaining_tasks})

    # Barchart data
    previous_data = PreviousMonth.objects.filter(user=request.user)
    dic_previous_data = {
        "Date": [x.date for x in previous_data],
        "Average": [y.average for y in previous_data]
    }

    df_previous = pd.DataFrame(dic_previous_data)
    barchart = px.bar(
        df_previous,
        x="Date",
        y="Average",
        title="Previous Month Averages",
        # labels={"x": "Date", "y": "Averages"}
    )
    barchart.update_xaxes(
        type='category',
        tickmode='auto',
        tickformat='%d %B (%a)<br>%Y',
        showline=True,
        showgrid=True,
        title_text="Date"
    )
    barchart.update_yaxes(
        title_text = "Averages"
    )
    barchart.update_layout(
        title={
            "font_size": 22,
            "xanchor": "center",
            "x": 0.5,
            "font": {"color": "blue"}
        }
    )
    barchart.update_layout(bargap=0.5, bargroupgap=0.5)
    barchart = barchart.to_html()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "DataVisualization/data.html",
                  {"progress_data": progress_data,
                   "chart": chart,
                   "pie": pie,
                   "barchart": barchart,
                   "page_obj": page_obj
                   }
                  )