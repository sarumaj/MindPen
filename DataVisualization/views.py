from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Endeavors.models import Endeavor
from To_Do.models import Task
from MyMood.models import DataMood
import plotly.express as px


@login_required()
def data(request):

    qs = DataMood.objects.filter(user=request.user)
    a = qs.count()
    # x = [x.mood_date for x in qs]
    fig = px.line(
        x=range(a),
        y=[int(y.mood_score) for y in qs],
        title="Mood Tracker",
        labels={"x": "Date", "y": "Mood"},
        markers=True
    )
    fig.update_layout(
        title={
            "font_size": 22,
            "xanchor": "center",
            "x": 0.5
        }
    )
    chart = fig.to_html()

    all_programs = Endeavor.objects.filter(author=request.user)
    progress_data = []

    for program in all_programs:
        all_tasks = Task.objects.filter(goal=program)  # Tasks for one program
        tasks = all_tasks.count()
        completed = all_tasks.filter(goal=program).filter(completed=True)   # Completed tasks for one program
        tasks_completed = completed.count()
        remaining_tasks = tasks - tasks_completed

        if tasks == 0:
            progress_percentage = 0
        else:
            progress_percentage = int((tasks_completed / tasks) * 100)

        progress_data.append({"program": program, "progress_percentage": progress_percentage,
                              "remaining_tasks": remaining_tasks})

    return render(request, "DataVisualization/data.html", {"progress_data": progress_data, "chart": chart})