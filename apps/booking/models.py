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
    day = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="2 PM")
    student = models.ForeignKey(CustomUser, related_name='student_appointments', on_delete=models.CASCADE, null=True, blank=True)
    booked = models.BooleanField(default=False)
    
    @property
    def get_weekday(self):
        return self.day.strftime("%A")

    def __str__(self):
        return f"{self.tutor} | day: {self.day} | time: {self.time}"
    
    def get_absolute_url(self):
        # returns a complete url string and let view handle the redirect
        return reverse("session-detail", kwargs={"pk": self.pk})
