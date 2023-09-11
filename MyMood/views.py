from django.utils import timezone
from django.shortcuts import render
from .models import DataMood
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from DataVisualization.models import PreviousMonth
from Endeavors.models import Endeavor
from To_Do.models import Task


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})

def mood(request):
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
        title=f"View of Your Mood for {now.strftime('%B')}",
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
        if mood.mood_score == -5:
            crying += 1
        elif mood.mood_score == -4:
            sad += 1
        elif mood.mood_score == -3:
            angry += 1
        elif mood.mood_score == -2:
            disappointed += 1
        elif mood.mood_score == -1:
            unhappy += 1
        elif mood.mood_score == 0:
            neutral += 1
        elif mood.mood_score == 1:
            happy += 1
        elif mood.mood_score == 2:
            very_happy += 1
        elif mood.mood_score == 3:
            joyful += 1
        elif mood.mood_score == 4:
            excited += 1
        elif mood.mood_score == 5:
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
    # fetch the data of the previous month
    previous_qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=previous_month)
    # previous exist calculate their average,
    # set new previous instance,
    # and delete that previous queryset
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

    # barchart data
    previous_data = PreviousMonth.objects.filter(user=request.user)
    dic_previous_data = {
        "Date": [x.date for x in previous_data],
        "Average": [y.average for y in previous_data]
    }

    df_previous = pd.DataFrame(dic_previous_data)
    barchart = px.bar(
        df_previous,
        y="Average",
        x="Date",
    )
    barchart.update_xaxes(
        type='category',
        tickmode='auto',
        tickformat='%d %B (%a)<br>%Y',
        showline=True,
        showgrid=True
    )
    barchart.update_layout(
        title={
            "text": "Previous Month Averages",
            "font_size": 22,
            "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
            "y":0.9,
            "font": {"color": "blue"},
        }
    )
    barchart.update_layout(bargap=0.5, bargroupgap=0.5)
    barchart = barchart.to_html()

    return render(request, "MyMood/mood.html", {"chart": chart, "pie": pie, "barchart": barchart})
