import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from apps.userprofile.models import CustomUser
from .models import Appointment


def daylist():
    days_list = []
    today = datetime.datetime.now()
    end_date = today + datetime.timedelta(days=14)

    for day_no in range(((end_date - today).days - 1)):
        days_data = {}
        curr_date = today + datetime.timedelta(days=day_no)
        weekday = curr_date.strftime("%A").upper()

        days_data["weekday"] = weekday
        days_data["date"] = curr_date.strftime("%Y-%m-%d")
        days_data["data"] = []

        tutors = CustomUser.objects.filter(
            is_tutor=True, tutor_appointments__date=curr_date
        ).distinct()
        if tutors:
            for tutor in tutors:
                tutor_data = {"name": tutor.username, "time_slots": []}
                appoints_in_day_for_tutor = Appointment.objects.filter(
                    tutor=tutor, booked=False, date=curr_date
                )
                if appoints_in_day_for_tutor:
                    for appoint_in_day_for_tutor in appoints_in_day_for_tutor:
                        appoint_id = appoint_in_day_for_tutor.id
                        time_slot = appoint_in_day_for_tutor.slot
                        if appoint_id not in tutor_data:
                            tutor_data["appoint_id"] = appoint_id
                        if time_slot not in tutor_data["time_slots"]:
                            tutor_data["time_slots"].append(time_slot)
                    days_data["data"].append(tutor_data)

            if weekday not in ["SATURDAY", "SUNDAY"]:
                days_list.append(days_data)
    print(days_list)
    return days_list


def home(request):
    context = {"days": daylist()}
    return render(request, "booking/home.html", context)


def aval_slots(request):
    appointments = Appointment.objects.all().filter(booked=False)
    context = {"appointments": appointments}
    return render(request, "booking/appointments.html", context)


def tutor(request, id):
    user = get_object_or_404(CustomUser, id=id)
    appointments = Appointment.objects.filter(tutor=user).order_by("date")
    context = {"user": user, "appointments": appointments}
    return render(request, "booking/tutor.html", context)


class TutorsListView(generic.ListView):
    queryset = CustomUser.objects.filter(
        is_tutor=True, tutor_appointments__isnull=False
    ).distinct()
    context_object_name = "tutors"
    template_name = "booking/tutors.html"


class BookAppointment(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Appointment, id=kwargs["pk"])
        booking.student = self.request.user
        booking.booked = True
        booking.save()
        messages.success(request, "You successfully booked an appointment.")
        return redirect("booking:aval_slots")
