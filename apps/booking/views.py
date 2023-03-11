from django.shortcuts import render

from .models import Appointment


def aval_slots(request):
    slots = Appointment.objects.all()
    context = {"slots": slots}
    return render(request, "booking/slots.html", context)
