from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from Accomplished.views import UpdateAccomplishedView, DeleteAccomplishedView
from Endeavors.views import add_endeavor, ListEndeavorView, DeleteEndeavorView, DetailEndeavorView, tasks
from Journaling.views import JournalListView, JournalDetailView, JournalUpdateView, JournalDeleteView
from To_Do.views import TaskListView, TaskDetailView, TaskDeleteView, TaskCreateView, TasklUpdateView
from MyMood.views import mood
from users.views import ProfileTemplateViews
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('DataVisualization.urls'), name='data'),



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
    path('create_endeavor/', add_endeavor, name='create_endeavor'),
    path('list_endeavor/', login_required(ListEndeavorView.as_view()), name='list_endeavor'),
    path('detail_endeavor/<pk>/detail/', login_required(DetailEndeavorView.as_view()), name='detail_endeavor'),
    path('delete_endeavor/<pk>/delete/', login_required(DeleteEndeavorView.as_view()), name='delete_endeavor'),
    path('tasks/', tasks, name='tasks'),


    # To-Do Routes
    path('todos/', TaskListView.as_view(), name='todos'),
    path('detail_todo/<int:pk>/detail/', TaskDetailView.as_view(), name='detail_todo'),
    path('delete_todo/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_todo'),
    path('create_todo/<str:program>/create', TaskCreateView.as_view(), name='create_todo'),
    path('update_todo/<int:pk>/update/', TasklUpdateView.as_view(), name='update_todo'),

    # Accomplished
    path('done/', include('Accomplished.urls'), name='done'),
    path('done_update/<int:pk>/', login_required(UpdateAccomplishedView.as_view()), name='done_update'),
    path('done_delete/<int:pk>/', login_required(DeleteAccomplishedView.as_view()), name='done_delete'),

    # MyMood
    path('mood/', login_required(mood), name='mood'),
]