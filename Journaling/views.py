from django.shortcuts import redirect
from django.views.generic import DetailView, DeleteView, ListView
from django.views.generic.edit import UpdateView
from .models import Journal
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import JournalModelForm


class JournalListView(ListView):
    paginate_by = 2
    model = Journal
    template_name = "Journaling/journal.html"

    def get_context_data(self, **kwargs):
        form = JournalModelForm(initial={"content": "Start journaling now! Share your thoughts, experiences, and memories right here."})
        context = super().get_context_data(**kwargs)
        context["posts"] = Journal.objects.filter(author=self.request.user)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = JournalModelForm(request.POST)
        if form.is_valid():
            form_journal = form.save(commit=False)
            form_journal.author = self.request.user
            form_journal.save()
            return redirect("journal")



# class JournalCreateView(CreateView):
#     model = Journal
#     template_name = "Journaling/journal.html"
#     fields = ["title", "content"]
#     success_url = "/journal/"
#     # paginate_by = 2
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts'] = Journal.objects.filter(author=self.request.user)
#         paginator = Paginator(context['posts'], 2)
#         page_number = self.request.GET.get('page')
#         context['page_obj'] = paginator.get_page(page_number)
#         return context
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
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
