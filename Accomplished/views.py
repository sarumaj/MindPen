from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Endeavors.models import Endeavor
from To_Do.models import Task
from .models import AccomplishedGoal
from .forms import SummaryModelForm
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator


@login_required()
def done(request):
    all_programs = Endeavor.objects.filter(author=request.user)
    for program in all_programs:
        all_tasks = Task.objects.filter(endeavor=program).count()
        all_completed_tasks = Task.objects.filter(endeavor=program).filter(completed=True).count()
        if (all_tasks != 0) and (all_tasks == all_completed_tasks):
            # Save a copy of the completed program in AccomplishedGoal model
            accomplished_program = AccomplishedGoal.objects.create(author=program.author,
                                                                   program_title=program.title,
                                                                   start_day=program.start_date,
                                                                   )
            accomplished_program.save()
            # Delete the completed program from the Endeavor model
            program.delete()
    accomplished_goal = AccomplishedGoal.objects.filter(author=request.user)
    paginator = Paginator(accomplished_goal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = SummaryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = SummaryModelForm()

    return render(request, "Accomplished/done.html", {"accomplished_goal": accomplished_goal, "form": form,
                                                      "page_obj": page_obj})


class UpdateAccomplishedView(UpdateView):
    model = AccomplishedGoal
    template_name = "Accomplished/accomplishedgoal_detail.html"
    fields = ["summary"]
    success_url = "/done/"


class DeleteAccomplishedView(UserPassesTestMixin, DeleteView):
    model = AccomplishedGoal
    template_name = "Accomplished/delete.html"
    success_url = "/done/"

    def test_func(self):
        accomplished = self.get_object()
        if self.request.user == accomplished.author:
            return True
        return False