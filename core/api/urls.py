from django.urls import path
from api.views import Notes, NoteDetails


urlpatterns = [
    path('', Notes.as_view()),
    path('<str:pk>', NoteDetails.as_view())
]