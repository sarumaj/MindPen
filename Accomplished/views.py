from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Endeavors.models import Endeavor
from To_Do.models import Task
from .models import AccomplishedGoal
from .forms import SummaryModelForm
from django.views.generic import UpdateView, DeleteView


@login_required()
def done(request):
    all_programs = Endeavor.objects.filter(author=request.user)
    for program in all_programs:
        all_tasks = Task.objects.filter(endeavor=program).count()
        all_completed_tasks = Task.objects.filter(endeavor=program).filter(completed=True).count()
        if all_tasks == all_completed_tasks:
            # Save a copy of the completed program in AccomplishedGoal model
            accomplished_program = AccomplishedGoal.objects.create(author=program.author,
                                                                   program_title=program.program_title,
                                                                   start_day=program.start_day,
                                                                   )
            accomplished_program.save()
            # Delete the completed program from the Endeavor model
            program.delete()
    accomplished_goal = AccomplishedGoal.objects.filter(author=request.user)
    if request.method == "POST":
        form = SummaryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = SummaryModelForm()

    return render(request, "Accomplished/done.html", {"accomplished_goal": accomplished_goal, "form": form})


# class UpdateDoneView(UpdateView):
#     model = AccomplishedGoal
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = SummaryModelForm
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = SummaryModelForm(request.POST)
#         if form.is_valid():
#             form_summary = form.save(commit=False)
#             form_summary.summary = self.request.summary
#             form.save()
#             return redirect("done")


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