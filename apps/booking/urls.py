from django.urls import path

from .views import BookAppointment, student_block_view, tutor_dashboard

app_name = "booking"

urlpatterns = [
    path("", student_block_view, name="student_block_view"),
    path("dashboard/", tutor_dashboard, name="tutor_dashboard"),
    path(
        "book-appointment/<int:appoint_id>/",
        BookAppointment.as_view(),
        name="book-appointment",
    ),
]