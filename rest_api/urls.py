from django.urls import include, path
from . import views

# # purpose of this router is to dynamically update URLs based on the the state of the DB backend
# router = routers.DefaultRouter()
# router.register(r'journalentries', views.ListCreateJournalEntriesView)
# # we can add additional routes to different serialised views here

urlpatterns = (
    # this line is what does the magic of including registered router URLs
    # we can add more version nums and modify responses accordingly
    path('journalentries/', views.ListCreateJournalEntriesView.as_view(), name='journal-entries-list-create'),
    path('journalentries/<int:pk>/', views.JournalEntriesDetailView.as_view(), name='journal-entries-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

