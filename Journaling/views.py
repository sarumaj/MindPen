from django.shortcuts import redirect
from django.views.generic import DetailView, DeleteView, ListView
from django.views.generic.edit import UpdateView
from .models import Journal, DataMood
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import JournalModelForm
from .filters import JournalFilter
from Habit_Tracker.views import journaling_frequency
from django.utils import timezone



class JournalListView(ListView):
    model = Journal
    template_name = "Journaling/journal.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        # journals of the current user
        queryset = queryset.filter(author=self.request.user)
        # create a filterset using JournalFilter and apply it to the queryset
        self.filterset = JournalFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # create an instance of JournalModelForm with initial data
        context = super().get_context_data(**kwargs)
        form = JournalModelForm()
        # add the form and search form (filterset form) to the context data
        context["form"] = form
        context["SearchForm"] = self.filterset.form
        # journaling frequency
        context["journaling_percentage"] = journaling_frequency(self.request.user)
        # User's last visit
        last_login = self.request.user.last_login
        last_logout = self.request.user.last_logout

        if last_logout is not None:
            time_away = last_login - last_logout
            days_diff = time_away.days
            context["days_diff"] = days_diff
            context["new_user"] = None  # No message for returning users
        else:
            context["days_diff"] = None  # No days difference available
            context["new_user"] = "This is your first visit 🌱"

        return context

    def post(self, request, *args, **kwargs):
        """ create a new journal """
        form = JournalModelForm(request.POST)
        if form.is_valid():
            # save the journal with the current user as the author
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
        # check if the currently logged-in user is the same as the author of the journal
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
        # check if the currently logged-in user is the same as the author of the journal
        journal = self.get_object()
        if self.request.user == journal.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        # Journal entry to be deleted
        journal = self.get_object()

        # Delete the related mood_score before deleting the journal entry
        DataMood.objects.filter(user=journal.author, mood_date=journal.journal_date).delete()

        # Delete the journal entry
        return super().delete(request, *args, **kwargs)
