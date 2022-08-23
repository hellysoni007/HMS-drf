from django.urls import path

from .views import PatientRegistrationView

urlpatterns = [
    path('', PatientRegistrationView.as_view(), name="patient-registration"),
    path('<int:pk>/', PatientRegistrationView.as_view(), name="patient-registration"),
]
