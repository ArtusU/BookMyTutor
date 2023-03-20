from django.db import models
from django.urls import reverse
#from django.contrib.auth.models import User

from apps.userprofile.models import Tutor, Student


TIME_CHOICES = (
    ("10 am", "10 am"),
    ("11 am", "11 am"),
    ("12 pm", "12 pm"),
    ("2 pm", "2 pm"),
    ("3 pm", "3 pm"),
    ("4 pm", "4 pm"),
)


class Appointment(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='tutor_appointments', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    slot = models.CharField(max_length=10, choices=TIME_CHOICES, null=True, blank=True)
    student = models.ForeignKey(Student, related_name='student_appointments', on_delete=models.CASCADE, null=True, blank=True)
    booked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student', 'booked')
    
    @property
    def get_weekday(self):
        return self.day.strftime("%A")

    def __str__(self):
        return f"{self.tutor} | date: {self.date} | slot: {self.slot} | student: {self.student} -> {self.booked}"
    


# class Session(models.Model):
#     tutor = models.ForeignKey(CustomUser, related_name='tutor_sessions', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     date = models.DateField(null=True, blank=True)
#     slot = models.CharField(max_length=10, choices=TIME_CHOICES, default="2 PM")
    
#     def __str__(self):
#         return f"{self.tutor} - {self.date} {self.slot}"


# class Booking(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     student = models.ForeignKey(CustomUser, related_name='student_bookings', on_delete=models.CASCADE)
#     date = models.DateField(auto_now=True)

#     def __str__(self):
#         return f"{self.student} -> {self.session}"
