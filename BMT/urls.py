from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("booking/", include("apps.booking.urls")),
    path('accounts/', include('allauth.urls')),  
]
