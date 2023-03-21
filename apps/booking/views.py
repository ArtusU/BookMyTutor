import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from apps.userprofile.models import Student, Tutor

from .models import Appointment


def daylist(tutor):
    """
    Returns:
    [
    {
        "weekday": "FRIDAY",
        "date": "2023-03-17",
        "data": [
            {"appoint_id": 38, "appoint_slot": "10 am"},
            {"appoint_id": 41, "appoint_slot": "2 pm"},
            {"appoint_id": 42, "appoint_slot": "3 pm"},
            {"appoint_id": 43, "appoint_slot": "4 pm"},
        ],
    },
    {
        "weekday": "THURSDAY",
        "date": "2023-03-23",
        "data": [
            {"appoint_id": 29, "appoint_slot": "12 pm"},
            {"appoint_id": 30, "appoint_slot": "2 pm"},
        ],
    },
    ]
    """
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    end_date = tomorrow + datetime.timedelta(days=15)
    days_list = []

    for day_no in range(((end_date - tomorrow).days)):
        days_data = {}
        curr_date = tomorrow + datetime.timedelta(days=day_no)
        weekday = curr_date.strftime("%A").upper()

        days_data["weekday"] = weekday
        days_data["date"] = curr_date.strftime("%Y-%m-%d")
        days_data["data"] = []

        if tutor:
            appoints = Appointment.objects.filter(
                tutor=tutor, date=curr_date
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

                if weekday not in ["SATURDAY", "SUNDAY"]:
                    days_data["data"] = sorted(days_data["data"], key=lambda k: k["appoint_slot"])
                    days_list.append(days_data)
    #print(days_list)
    return days_list


@login_required
def student_block_view(request):
    user_student = request.user
    student_obj = Student.objects.get(user=user_student)
    tutor = student_obj.tutor
    context = {"days": daylist(tutor=tutor), "tutor": tutor}
    print(context)
    return render(request, "booking/home.html", context)


class BookAppointment(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Appointment, pk=kwargs["appoint_id"])
        student = Student.objects.get(user=self.request.user)
        booking.student = student
        booking.booked = True
        try:
            booking.save()
            messages.success(
                self.request,
                "You have successfully booked an appointment for {} on {}".format(
                    booking.slot, booking.date
                ),
            )
        except IntegrityError:
            messages.warning(
                self.request,
                "You can only book one appointment at a time. If you wish to book a new appointment, please go to your booking and cancel your current appointment and try booking again."
                ),
            return redirect("booking:student_block_view")  
        return redirect("booking:student_block_view")


class StudentBookingList(LoginRequiredMixin, generic.ListView):
    template_name = "booking/student_booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)
        queryset = Appointment.objects.filter(student=student, booked=True).order_by('date')
        return queryset


class CancelAppointment(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Appointment, pk=kwargs["booking_id"])
        booking.student = None
        booking.booked = False
        booking.save()
        messages.success(
            request,
            "You have successfully canceled an appointment for {} on {}".format(
                booking.slot, booking.date
            ),
        )
        return redirect("booking:booking_list")


def tutdaylist(tutor):
    """
    Returns:
    [
    {"weekday": "MONDAY", "date": "2023-03-20", "data": []},
    {"weekday": "TUESDAY", "date": "2023-03-21", "data": []},
    {
        "weekday": "WEDNESDAY",
        "date": "2023-03-22",
        "data": [
            {"appoint_id": 126, "appoint_slot": "11 am", "appoint_booked": False},
            {"appoint_id": 127, "appoint_slot": "12 pm", "appoint_booked": False},
            {"appoint_id": 128, "appoint_slot": "14 pm", "appoint_booked": False},
            {"appoint_id": 129, "appoint_slot": "15 pm", "appoint_booked": False},
        ],
    },
    {
        "weekday": "THURSDAY",
        "date": "2023-03-23",
        "data": [
            {"appoint_id": 132, "appoint_slot": "11 am", "appoint_booked": False},
            {"appoint_id": 133, "appoint_slot": "12 pm", "appoint_booked": False},
            {"appoint_id": 134, "appoint_slot": "14 pm", "appoint_booked": False},
            {"appoint_id": 135, "appoint_slot": "15 pm", "appoint_booked": False},
        ],
    },
    {"weekday": "FRIDAY", "date": "2023-03-24", "data": []},
    {"weekday": "MONDAY", "date": "2023-03-27", "data": []},
    {"weekday": "TUESDAY", "date": "2023-03-28", "data": []},
    {"weekday": "WEDNESDAY", "date": "2023-03-29", "data": []},
    {"weekday": "THURSDAY", "date": "2023-03-30", "data": []},
    {"weekday": "FRIDAY", "date": "2023-03-31", "data": []},
    ]
    """
    today = datetime.datetime.now()
    end_date = today + datetime.timedelta(days=14)
    days_list = []

    for day_no in range(((end_date - today).days)):
        days_data = {}
        curr_date = today + datetime.timedelta(days=day_no)
        weekday = curr_date.strftime("%A").upper()

        days_data["weekday"] = weekday
        days_data["date"] = curr_date.strftime("%Y-%m-%d")
        days_data["data"] = []
        if tutor:
            appoints = Appointment.objects.filter(tutor=tutor, date=curr_date)
            if appoints:
                for appoint in appoints:
                    appoint_id = appoint.id
                    appoint_slot = appoint.slot
                    appoint_booked = appoint.booked
                    tutor_data = {}
                    tutor_data["appoint_id"] = []
                    tutor_data["appoint_slot"] = []
                    tutor_data["appoint_booked"] = []
                    if appoint_id not in tutor_data["appoint_id"]:
                        tutor_data["appoint_id"] = appoint_id
                    if appoint_slot not in tutor_data["appoint_slot"]:
                        tutor_data["appoint_slot"] = appoint_slot
                    if appoint_booked not in tutor_data["appoint_booked"]:
                        tutor_data["appoint_booked"] = appoint_booked
                    days_data["data"].append(tutor_data)

            if weekday not in ["SATURDAY", "SUNDAY"]:
                days_data["data"] = sorted(
                    days_data["data"], key=lambda k: k["appoint_slot"]
                )
                days_list.append(days_data)
    #print(days_list)
    return days_list


@login_required
def create_appoints_day(request, date):
    slots = ["10 am", "11 am", "12 pm", "14 pm", "15 pm", "16 pm"]
    user_tutor = request.user
    tutor = Tutor.objects.get(user=user_tutor)
    for slot in slots:
        if not Appointment.objects.filter(tutor=tutor, date=date, slot=slot).exists():
            appoint = Appointment.objects.create(tutor=tutor, date=date, slot=slot)
            appoint.save()
    return redirect("booking:tutor_dashboard")


@login_required
def tutor_dashboard(request):
    user_tutor = request.user
    tutor = Tutor.objects.get(user=user_tutor)
    context = {"days": tutdaylist(tutor=tutor)}
    return render(request, "booking/tutor_dashboard.html", context)


@login_required
def delete_appointment(request, date, slot):
    user_tutor = request.user
    tutor = Tutor.objects.get(user=user_tutor)
    appointment = Appointment.objects.filter(tutor=tutor, date=date, slot=slot)
    appointment.delete()
    messages.success(
        request,
        "You have successfully deleted appointment for {} on {}".format(slot, date),
    )
    return redirect("booking:tutor_dashboard")


class TutorAppointmentList(LoginRequiredMixin, generic.ListView):
    template_name = "booking/tutor_appointment_list.html"
    context_object_name = "appointments"
    # queryset = Appointment.objects.filter(booked=True)

    def get_queryset(self):
        user = self.request.user
        tutor = Tutor.objects.get(user=user)
        queryset = Appointment.objects.filter(tutor=tutor, booked=True)
        return queryset
