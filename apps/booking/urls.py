from django.urls import path

from .views import aval_slots, tutor

app_name = 'booking'

urlpatterns = [
    path("", aval_slots, name="aval_slots"),   
    path("tutor/<int:id>/", tutor, name="tutor"),   
]