from django.utils import timezone
from django.shortcuts import render
from .models import DataMood, PreviousMonth
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from Journaling.models import Journal
# from transformers import AutoTokenizer
# from transformers import AutoModelForSequenceClassification
from transformers import pipeline
import joblib


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})

def mood(request):
    # get the current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    total = count = 0

    """added for MindPen"""
    # Load the saved pipeline
    loaded_pipe = joblib.load("Machine_Learning\sentiment_analysis_pipeline.joblib")
    qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=month)
    previous_positive_count = qs.filter(mood_score=1).count()
    previous_negative_count = qs.filter(mood_score=0).count()

    the_input = Journal.objects.filter(author=request.user).first()
    if the_input:
        lastest_journal = the_input.content

        # a new journal entry
        if not the_input.processed:

            # Sentiment analysis for the new journal entry
            predicted_sentiment = loaded_pipe.predict([lastest_journal])
            current_sentiment = predicted_sentiment[0]

            # Transform the "POS/Neg" to "0/1" and save it in the MOOD DB
            if current_sentiment == "POSITIVE":
                inferred_mood = 1
            else:
                inferred_mood = 0

            mood_entry = DataMood(
                # Link to the currently signed in user
                user=request.user,
                # Save the inferred mood (positive/negative)
                mood_score=inferred_mood,
                # Timestamp for when the mood is saved
                mood_date=timezone.now()
            )
            # processed journal
            the_input.processed = True
            the_input.save()
            mood_entry.save()

            if current_sentiment == "POSITIVE":
                previous_positive_count += 1
            else:
                previous_negative_count += 1

        labels = ["Positive", "Negative"]
        values = [previous_positive_count, previous_negative_count]
        colors = ["green", "red"]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                    marker=dict(colors=colors), hole=.5,
                                    textinfo="label+percent",
                                    insidetextorientation="radial"
                                     )])
    else:
        fig = go.Figure(data=[go.Pie(labels=["Nothing to Display"],
                                     values=[1], hole=.5,
                                     marker_colors=["gray"],
                                     textinfo = "label+percent",
                                     insidetextorientation = "radial"
                                     )])
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
            # "text": "Previous Month Averages",
            # "font_size": 22,
            # "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
            "y": 0.9,
            "font": {"color": "blue"},
        }
    )
    barchart.update_layout(bargap=0.5, bargroupgap=0.5)
    barchart = barchart.to_html()

    return render(request, "MyMood/mood.html", {"pie": pie, "barchart": barchart})


