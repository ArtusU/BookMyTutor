from django.db import models
from django.urls import reverse
#from django.contrib.auth.models import User

from apps.userprofile.models import CustomUser


# SERVICE_CHOICES = (
#     ("Consultation", "Consultation"),
#     ("Mentoring", "Mentoring"),
# )

TIME_CHOICES = (
    ("2 PM", "2 PM"),
    ("2:30 PM", "2:30 PM"),
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
)


class Appointment(models.Model):
    tutor = models.ForeignKey(CustomUser, related_name='tutor_appointments', on_delete=models.CASCADE)
    #type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Consultation")
    date = models.DateField(null=True, blank=True)
    slot = models.CharField(max_length=10, choices=TIME_CHOICES, default="2 PM")
    student = models.ForeignKey(CustomUser, related_name='student_appointments', on_delete=models.CASCADE, null=True, blank=True)
    booked = models.BooleanField(default=False)
    
    @property
    def get_weekday(self):
        return self.day.strftime("%A")

    def __str__(self):
        return f"{self.tutor} | date: {self.date} | slot: {self.slot}"
    
    def get_absolute_url(self):
        # returns a complete url string and let view handle the redirect
        return reverse("session-detail", kwargs={"pk": self.pk})



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
