from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from apps.userprofile.models import CustomUser
from .models import Appointment


def aval_slots(request):
    slots = Appointment.objects.all().filter(booked=False)
    context = {"slots": slots}
    return render(request, "booking/slots.html", context)


def tutor(request, id):
    user = get_object_or_404(CustomUser, id=id)
    slots = Appointment.objects.filter(tutor=user).order_by("day")
    context = {"user": user, "slots": slots}
    return render(request, "booking/tutor.html", context)


class TutorsListView(generic.ListView):
    queryset = CustomUser.objects.filter(is_tutor=True, tutor_appointments__isnull=False).distinct()
    context_object_name = 'tutors'
    template_name = 'booking/tutors.html'
    

class BookAppointment(LoginRequiredMixin, generic.View): 
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Appointment, id=kwargs['pk'])
        booking.student = self.request.user
        booking.booked = True
        booking.save()
        messages.success(request, 'You successfully booked an appointment.')
        return redirect("booking:aval_slots")
    
