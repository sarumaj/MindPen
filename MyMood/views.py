from django.utils import timezone
from django.shortcuts import render
from .models import DataMood, PreviousMonth
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import joblib
from SentimentAnalysis.consumers import (
    analyze_last_journal_sentiment,
    get_last_journal_for_user,
)
from Habit_Tracker.views import journaling_frequency
from Quote.views import get_quote


def mood_message(request):
    time = timezone.now()
    return render(request, "MyMood/mood_message.html", {"time": time})


# Load the saved SVM pipeline
loaded_pipe = joblib.load(r"Machine_Learning/svm_pipeline.joblib")


def either_Remote_or_SVM(request):
    dic_sentiment = None

    try:
        # try to reach Remote API
        dic_sentiment = analyze_last_journal_sentiment(request)
        if dic_sentiment:
            return dic_sentiment

    except Exception as e:
        # Log the failure
        print(f"Remote API failed: {e}")

        # if Remote fails use SVM pipeline
        last_journal = get_last_journal_for_user(request)
        if last_journal:
            journal_text = last_journal.content
            predicted_sentiment = loaded_pipe.predict([journal_text])[0]
            dic_sentiment = {"sentiment": predicted_sentiment}
            last_journal.processed = True
            last_journal.save()

    return dic_sentiment


def process_sentiment(request):
    # current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    month_str = now.strftime("%B")
    total = count = 0

    # Query previous mood counts for the current user
    qs = DataMood.objects.filter(
        user=request.user, mood_date__year=year, mood_date__month=month
    )
    previous_positive_count = qs.filter(mood_score=1).count()
    previous_negative_count = qs.filter(mood_score=-1).count()
    previous_neutral_count = qs.filter(mood_score=0).count()

    # the returned sentiment from Remote or SVM
    dic_sentiment = either_Remote_or_SVM(request)

    if dic_sentiment:

        # set the inferred mood accordingly
        sentiment_label = dic_sentiment["sentiment"]
        print(f"Predicted sentiment: {sentiment_label}")
        if sentiment_label == "positive":
            inferred_mood = 1
            previous_positive_count += 1
        elif sentiment_label == "negative":
            inferred_mood = -1
            previous_negative_count += 1
        else:
            inferred_mood = 0
            previous_neutral_count += 1

        # Save the inferred mood
        mood_entry = DataMood(
            user=request.user, mood_score=inferred_mood, mood_date=timezone.now()
        )
        mood_entry.save()

    mood_exists = any(
        [previous_positive_count, previous_negative_count, previous_neutral_count]
    )
    if mood_exists:
        # pie chart
        labels = ["Positive", "Negative", "Neutral"]
        values = [
            previous_positive_count,
            previous_negative_count,
            previous_neutral_count,
        ]
        colors = ["green", "red", "yellow"]
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels, values=values, marker=dict(colors=colors), hole=0.5
                )
            ]
        )
    else:

        # default pie chart if no journals are available
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Nothing to Display"],
                    values=[1],
                    hole=0.5,
                    marker_colors=["gray"],
                )
            ]
        )
    pie = fig.to_html()

    # set the variables according to the month
    if month == 1:
        year, previous_month = year - 1, 12
    else:
        previous_month = month - 1

    """    fetch the data of the previous month set new previous instance,
        and delete that previous queryset
    """
    previous_qs = DataMood.objects.filter(
        user=request.user, mood_date__year=year, mood_date__month=previous_month
    )
    if previous_qs:
        for entry in previous_qs:
            total += entry.mood_score
            count += 1
        average = round(total / count, 2)
        previous = PreviousMonth(
            user=request.user, average=average, date=f"{year}-{previous_month:02d}"
        )
        previous.save()
        previous_qs.delete()

    # bar chart data
    previous_data = PreviousMonth.objects.filter(user=request.user)
    dic_previous_data = {
        "Date": [x.date for x in previous_data],
        "Average Mood Score": [y.average for y in previous_data],
    }
    df_previous = pd.DataFrame(dic_previous_data)
    barchart = px.bar(df_previous, y="Average Mood Score", x="Date", text_auto=True)
    barchart.update_layout(
        bargap=0.5,
        bargroupgap=0.5,
        yaxis=dict(range=[-1, 1]),
        xaxis=dict(tickformat="%b %Y"),
    )
    barchart = barchart.to_html()

    # today's quote
    quote = get_quote()

    # journaling_frequency
    user = request.user
    journaling_percentage = journaling_frequency(user)

    # User's last visit
    last_login = request.user.last_login
    last_logout = request.user.last_logout

    if last_logout is not None:
        time_away = last_login - last_logout
        days_diff = time_away.days
        new_user = None
    else:
        days_diff = None
        new_user = "This is your first visit 🌱"

    return render(
        request,
        "MyMood/mood.html",
        {
            "pie": pie,
            "barchart": barchart,
            "journaling_percentage": journaling_percentage,
            "month_str": month_str,
            "days_diff": days_diff,
            "new_user": new_user,
            "quote": quote,
        },
    )
