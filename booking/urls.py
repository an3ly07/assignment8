from django.urls import path
from .views import (
    home,
    slots_page,
    specialization_page,
    provider_detail,
    slots_api,
    providers_api,
    bookings_api,
)

urlpatterns = [
    # 🧑 USER SITE
    path('', home, name='home'),
    path('slots/', slots_page, name='slots'),
    path('specialization/<str:name>/', specialization_page, name='specialization'),
    path('provider/<int:provider_id>/', provider_detail, name='provider_detail'),

    # 🔌 API
    path('api/slots/', slots_api),
    path('api/slots/<int:slot_id>/', slots_api),
    path('api/providers/', providers_api),
    path('api/providers/<int:provider_id>/', providers_api),
    path('api/bookings/', bookings_api),
    path('api/bookings/<int:booking_id>/', bookings_api),
]
