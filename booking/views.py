from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TimeSlot
import json


def home(request):
    return render(request, 'booking/home.html')


def slots_page(request):
    slots = TimeSlot.objects.all()
    return render(request, 'booking/slots.html', {'slots': slots})


@csrf_exempt
def slots_api(request, slot_id=None):

    if request.method == 'GET':
        slots = TimeSlot.objects.all()
        data = [{
            'id': s.id,
            'provider': str(s.provider),
            'start_time': s.start_time,
            'is_booked': s.is_booked
        } for s in slots]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        slot = TimeSlot.objects.create(
            provider_id=data['provider_id'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        return JsonResponse({'status': 'created'})

    if request.method == 'PUT' and slot_id:
        slot = TimeSlot.objects.get(id=slot_id)
        data = json.loads(request.body)
        slot.is_booked = data['is_booked']
        slot.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE' and slot_id:
        TimeSlot.objects.get(id=slot_id).delete()
        return JsonResponse({'status': 'deleted'})
