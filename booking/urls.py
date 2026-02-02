from django.urls import path
from .views import home, slots_page, slots_api

urlpatterns = [
    # 🧑 USER SITE
    path('', home, name='home'),
    path('slots/', slots_page, name='slots'),

    # 🔌 API
    path('api/slots/', slots_api),
    path('api/slots/<int:slot_id>/', slots_api),
]
