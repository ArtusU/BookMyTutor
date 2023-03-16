import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from apps.userprofile.models import Student, Tutor

from .models import Appointment


def daylist(tutor, booked):
    today = datetime.datetime.now()
    end_date = today + datetime.timedelta(days=14)
    days_list = []

    for day_no in range(((end_date - today).days - 1)):
        days_data = {}
        curr_date = today + datetime.timedelta(days=day_no)
        weekday = curr_date.strftime("%A").upper()

        days_data["weekday"] = weekday
        days_data["date"] = curr_date.strftime("%Y-%m-%d")
        days_data["data"] = []

        if tutor:
            appoints = Appointment.objects.filter(
                tutor=tutor, booked=booked, date=curr_date
            )
            if appoints:
                for appoint in appoints:
                    appoint_id = appoint.id
                    appoint_slot = appoint.slot
                    tutor_data = {}
                    tutor_data["appoint_id"] = []
                    tutor_data["appoint_slot"] = []
                    if appoint_id not in tutor_data["appoint_id"]:
                        tutor_data["appoint_id"] = appoint_id
                    if appoint_slot not in tutor_data["appoint_slot"]:
                        tutor_data["appoint_slot"] = appoint_slot
                    days_data["data"].append(tutor_data)

            if days_data["data"]:
                if weekday not in ["SATURDAY", "SUNDAY"]:
                    days_list.append(days_data)
    print(days_list)
    return days_list


@login_required
def student_block_view(request):
    user_student = request.user
    student_obj = Student.objects.get(user=user_student)
    tutor = student_obj.tutor
    context = {"days": daylist(tutor=tutor, booked=False), "tutor": tutor}
    return render(request, "booking/home.html", context)


class BookAppointment(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Appointment, pk=kwargs["appoint_id"])
        student = Student.objects.get(user=self.request.user)
        booking.student = student
        booking.booked = True
        booking.save()
        messages.success(
            request,
            "You have successfully booked an appointment for {} on {}".format(
                booking.slot, booking.date
            ),
        )
        return redirect("booking:student_block_view")


@login_required
def tutor_dashboard(request):
    user_tutor = request.user
    tutor = Tutor.objects.get(user=user_tutor)
    context = {"days": daylist(tutor=tutor, booked=True)}
    return render(request, "booking/tutor_dashboard.html", context)