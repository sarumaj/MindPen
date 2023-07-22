from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from Endeavors.views import CreateEndeavorView, ListEndeavorView, DeleteEndeavorView, DetailEndeavorView
from Journaling.views import JournalListView, JournalDetailView, JournalUpdateView, JournalDeleteView
from To_Do.views import TaskListView, TaskDetailView, TaskDeleteView, TaskCreateView, TasklUpdateView
from MyMood.views import MoodFromView
from users.views import ProfileTemplateViews
from django.contrib.auth.decorators import login_required
from Endeavors.views import endeavor_task_forms


urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('DataVisualization.urls'), name='data'),
    path('mood/', login_required(MoodFromView.as_view()), name='mood'),
    path('done/', include('Accomplished.urls'), name='done'),

    # user's routes
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', login_required(ProfileTemplateViews.as_view()), name='profile'),
    path('register/', include('users.urls')),

    # Journaling Routes
    path('journal/<int:pk>/', login_required(JournalDetailView.as_view()), name='journal_detail'),
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal_update'),
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal_delete'),
    path('journal/', login_required(JournalListView.as_view()), name='journal'),

    # Endeavor Routes
    path('create_endeavor/', login_required(CreateEndeavorView.as_view()), name='create_endeavor'),
    path('list_endeavor/', login_required(ListEndeavorView.as_view()), name='list_endeavor'),
    path('detail_endeavor/<pk>/detail/', login_required(DetailEndeavorView.as_view()), name='detail_endeavor'),
    path('delete_endeavor/<pk>/delete/', login_required(DeleteEndeavorView.as_view()), name='delete_endeavor'),
    path('programtask/', endeavor_task_forms, name='programtask'),


    # To-Do Routes
    path('todos/', TaskListView.as_view(), name='todos'),
    path('detail_todo/<int:pk>/detail/', TaskDetailView.as_view(), name='detail_todo'),
    path('delete_todo/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_todo'),
    path('create_todo/', TaskCreateView.as_view(), name='create_todo'),
    path('update_todo/<int:pk>/update/', TasklUpdateView.as_view(), name='update_todo'),
]