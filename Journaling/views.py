from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import DetailView, DeleteView, ListView
from django.views.generic.edit import UpdateView
from .models import Journal
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import JournalModelForm
from .filters import JournalFilter


class JournalListView(ListView):
    model = Journal
    template_name = "Journaling/journal.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        self.filterset = JournalFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = JournalModelForm(initial={"content": "Start journaling now! Share your thoughts,"
                                                    " experiences, and memories right here.",
                                         "title": "Journal Title"})
        context["form"] = form
        context["SearchForm"] = self.filterset.form
        return context

    def post(self, request, *args, **kwargs):
        form = JournalModelForm(request.POST)
        if form.is_valid():
            form_journal = form.save(commit=False)
            form_journal.author = self.request.user
            form_journal.save()
            return redirect("journal")


class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Journal
    template_name = "Journaling/update.html"
    fields = ["title", "content"]
    success_url = "/journal/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        journal = self.get_object()
        if self.request.user == journal.author:
            return True
        return False


class JournalDetailView(DetailView):
    model = Journal
    template_name = "Journaling/detail_journal.html"
    context_object_name = "post"


class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Journal
    template_name = "Journaling/delete.html"
    success_url = "/journal/"

    def test_func(self):
        journal = self.get_object()
        if self.request.user == journal.author:
            return True
        return False
