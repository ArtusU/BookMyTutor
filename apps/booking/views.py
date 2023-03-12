from django.shortcuts import get_object_or_404, render

from .models import Appointment
from apps.userprofile.models import CustomUser


def aval_slots(request):
    slots = Appointment.objects.all()
    context = {"slots": slots}
    return render(request, "booking/slots.html", context)


def tutor(request, id):
    user = get_object_or_404(CustomUser, id=id)
    slots = Appointment.objects.filter(tutor=user).order_by("day")
    context = {"user": user, "slots": slots}
    return render(request, "booking/tutor.html", context)


def make_appointment():
    pass