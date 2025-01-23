from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


from Journaling.views import JournalListView, JournalDetailView, JournalUpdateView, JournalDeleteView
from MyMood.views import process_sentiment,  mood_message
from users.views import ProfileTemplateViews
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),



    # user's routes
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', login_required(ProfileTemplateViews.as_view()), name='profile'),
    path('register/', include('users.urls')),
    path('sms/', include('SMS.urls')),

    # Journaling Routes
    path('journal/<int:pk>/', login_required(JournalDetailView.as_view()), name='journal_detail'),
    path('journal/<int:pk>/update/', JournalUpdateView.as_view(), name='journal_update'),
    path('journal/<int:pk>/delete/', JournalDeleteView.as_view(), name='journal_delete'),
    path('journal/', login_required(JournalListView.as_view()), name='journal'),


    # MyMood
    path('mood/', login_required(process_sentiment), name='mood'),
    path('mood_msg/', mood_message, name='mood_msg'),
]