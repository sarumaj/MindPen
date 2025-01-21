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
from SA_Deepgram.consumers import analyze_last_journal_sentiment


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})

def mood(request):
    # get the current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    total = count = 0

    # Load the saved pipeline
    # loaded_pipe = joblib.load("Machine_Learning\sentiment_analysis_pipeline.joblib")


    qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=month)
    previous_positive_count = qs.filter(mood_score=1).count()
    previous_negative_count = qs.filter(mood_score=-1).count()
    previous_neutral_count = qs.filter(mood_score=0).count()

    # Deepgram performs SA for the last unprocessed journal
    dic_sentiment = analyze_last_journal_sentiment(request)

    if dic_sentiment:

        # use the returned sentiment to set the inferred_mood
        sentiment_label = dic_sentiment["sentiment"]
        if sentiment_label == "positive":
            inferred_mood = 1
            previous_positive_count += 1
        elif sentiment_label == "negative":
            inferred_mood = -1
            previous_negative_count += 1
        else:
            inferred_mood = 0
            previous_neutral_count += 1

        # save the inferred mood
        mood_entry = DataMood(
            user=request.user,
            mood_score=inferred_mood,
            mood_date=timezone.now()
        )
        mood_entry.save()

        # pie chart
        labels = ["Positive", "Negative", "Neutral"]
        values = [previous_positive_count, previous_negative_count, previous_neutral_count]
        colors = ["green", "red", "yellow"]
        fig = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors), hole=0.5)])
    else:
        # default pie chart if no journals are available
        fig = go.Figure(data=[go.Pie(
            labels=["Nothing to Display"], values=[1],
            hole=0.5, marker_colors=["gray"])])
    pie = fig.to_html()

    # set the variables according to the month
    if month == 1:
        year, previous_month = year - 1, 12
    else:
        previous_month = month - 1

    # fetch the data of the previous month
    # set new previous instance,
    # and delete that previous queryset
    previous_qs = DataMood.objects.filter(user=request.user, mood_date__year=year, mood_date__month=previous_month)
    if previous_qs:
        for entry in previous_qs:
            total += entry.mood_score
            count += 1
        average = round(total / count, 2)
        previous = PreviousMonth(user=request.user, average=average, date=f"{year}-{previous_month:02d}")
        previous.save()
        previous_qs.delete()

    # bar chart data
    previous_data = PreviousMonth.objects.filter(user=request.user)
    dic_previous_data = {
        "Date": [x.date for x in previous_data],
        "Average": [y.average for y in previous_data],
    }
    df_previous = pd.DataFrame(dic_previous_data)
    barchart = px.bar(df_previous, y="Average", x="Date")
    barchart.update_layout(bargap=0.5, bargroupgap=0.5)
    barchart = barchart.to_html()

    return render(request, "MyMood/mood.html", {"pie": pie, "barchart": barchart})
