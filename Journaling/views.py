from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import JournalModelForm
from .models import Journal


class JournalModelFromView(View):
    template_name = "Journaling/journal.html"

    def get(self, request, *args, **kwargs):
        journal_form = JournalModelForm()
        posts = Journal.objects.all()
        return render(request, self.template_name, {"journal_form": journal_form, "posts": posts})

    def post(self, request, *args, **kwargs):
        journal_form = JournalModelForm(request.POST)
        if journal_form.is_valid():
            journal_form.save()
            return redirect("journal")
        posts = Journal.objects.all()
        return render(request, self.template_name, {"journal_form": journal_form, "posts": posts})


class JournalDetailView(DetailView):
    model = Journal
    template_name = "Journaling/detail_journal.html"
    context_object_name = "post"


class JournalUpdateView(UpdateView):
    model = Journal
    form_class = JournalModelForm
    template_name = "Journaling/update.html"
    success_url = "/journal/"


class JournalDeleteView(DeleteView):
    model = Journal
    template_name = "Journaling/delete.html"
    success_url = "/journal/"
