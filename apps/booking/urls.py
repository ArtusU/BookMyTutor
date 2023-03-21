from django.urls import path

from .views import (
    TutorAppointmentList,
    BookAppointment,
    CancelAppointment,
    StudentBookingList,
    student_block_view,
    tutor_dashboard,
    create_appoints_day,
    delete_appointment,
)

app_name = "booking"

urlpatterns = [
    # Student
    path("", student_block_view, name="student_block_view"),
    path(
        "book_appointment/<int:appoint_id>/",
        BookAppointment.as_view(),
        name="book_appointment",
    ),
    path(
        "cancel_appointment/<int:booking_id>/",
        CancelAppointment.as_view(),
        name="cancel_appointment",
    ),
    path(
        "booking_list/",
        StudentBookingList.as_view(),
        name="booking_list",
    ),
    # Tutor
    path("dashboard/", tutor_dashboard, name="tutor_dashboard"),
    path(
        "dashboard/appointment_list/",
        TutorAppointmentList.as_view(),
        name="appointment_list",
    ),
    path(
        "create/appointments/<date>/", create_appoints_day, name="create_appointments"
    ),
    path(
        "delete/appointments/<date>/<slot>/",
        delete_appointment,
        name="delete_appointment",
    ),
]
