from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

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
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Consultation")
    booked = models.BooleanField(default=False)
    day = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="2 PM")

    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
