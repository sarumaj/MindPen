from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Endeavors.models import Endeavor
from To_Do.models import Task
from django.core.paginator import Paginator


@login_required()
def data(request):
    # Progress bar
    all_programs = Endeavor.objects.filter(author=request.user)
    progress_data = []
    for program in all_programs:
        all_tasks = Task.objects.filter(endeavor=program)
        tasks = all_tasks.count()
        completed = all_tasks.filter(endeavor=program).filter(completed=True)
        tasks_completed = completed.count()
        remaining_tasks = tasks - tasks_completed

        # calculate percentages
        if tasks == 0:
            progress_percentage = 0
        else:
            progress_percentage = int((tasks_completed / tasks) * 100)

        progress_data.append({
            "program": program,
            "progress_percentage": progress_percentage,
            "remaining_tasks": remaining_tasks})

    paginator = Paginator(progress_data, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "DataVisualization/data.html", {
        "progress_data": progress_data,
        "page_obj": page_obj})
