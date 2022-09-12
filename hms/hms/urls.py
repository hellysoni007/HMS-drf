from django.urls import path, include

urlpatterns = [
    path('', include('account.urls')),
    path('patients/', include('patients.urls')),
    path('operation/', include('operation.urls')),
    path('bill/', include('billing.urls'))
]
