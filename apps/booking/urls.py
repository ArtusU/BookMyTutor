from django.urls import path

from .views import appointments_list, tutor, week, BookAppointment, TutorsListView

app_name = "booking"

urlpatterns = [
    path("list/", appointments_list, name="appointments_list"),
    path("", week, name="week"),
    path("tutor/<int:id>/", tutor, name="tutor"),
    path("tutors/", TutorsListView.as_view(), name="tutors"),
    path(
        "book-appointment/<int:pk>/", BookAppointment.as_view(), name="book-appointment"
    ),
]
