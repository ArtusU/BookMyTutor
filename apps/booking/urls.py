from django.urls import path

from .views import aval_slots, tutor, BookAppointment

app_name = 'booking'

urlpatterns = [
    path("", aval_slots, name="aval_slots"),   
    path("tutor/<int:id>/", tutor, name="tutor"),   
    path("book-appointment/<int:pk>/", BookAppointment.as_view(), name="book-appointment"),   
]