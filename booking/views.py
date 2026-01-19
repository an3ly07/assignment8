from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
import json

@csrf_exempt
def bookings_api(request):
    if request.method == 'GET':
        data = list(Booking.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        booking = Booking.objects.create(
            client_id=data['client_id'],
            time_slot_id=data['time_slot_id']
        )
        return JsonResponse({'id': booking.id})
