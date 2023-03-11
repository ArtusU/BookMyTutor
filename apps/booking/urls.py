from django.urls import path

from .views import aval_slots

app_name = 'booking'

urlpatterns = [
    path("", aval_slots, name="aval_slots"),   
]