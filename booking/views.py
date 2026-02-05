from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Provider, TimeSlot, Booking
import json


def home(request):
    return render(request, 'booking/home.html')


def slots_page(request):
    slots = TimeSlot.objects.select_related('provider').all()
    return render(request, 'booking/slots.html', {'slots': slots})


def specialization_page(request, name):
    slots = TimeSlot.objects.filter(
        provider__specialization__iexact=name
    ).select_related('provider')
    return render(
        request,
        'booking/specialization.html',
        {'slots': slots, 'specialization': name.capitalize()},
    )


def provider_detail(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    slots = TimeSlot.objects.filter(provider=provider).order_by('start_time')
    return render(
        request,
        'booking/doctor.html',
        {'provider': provider, 'slots': slots},
    )


# ---------- API: Slots ----------
@csrf_exempt
def slots_api(request, slot_id=None):
    if request.method == 'GET':
        if slot_id is not None:
            slot = get_object_or_404(TimeSlot, id=slot_id)
            data = {
                'id': slot.id,
                'provider_id': slot.provider_id,
                'provider': str(slot.provider),
                'start_time': slot.start_time.isoformat(),
                'end_time': slot.end_time.isoformat(),
                'is_booked': slot.is_booked,
            }
            return JsonResponse(data)
        slots = TimeSlot.objects.select_related('provider').all()
        data = [
            {
                'id': s.id,
                'provider_id': s.provider_id,
                'provider': str(s.provider),
                'start_time': s.start_time.isoformat(),
                'end_time': s.end_time.isoformat(),
                'is_booked': s.is_booked,
            }
            for s in slots
        ]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        slot = TimeSlot.objects.create(
            provider_id=data['provider_id'],
            start_time=data['start_time'],
            end_time=data['end_time'],
        )
        return JsonResponse({'id': slot.id, 'status': 'created'}, status=201)

    if request.method == 'PUT' and slot_id is not None:
        slot = get_object_or_404(TimeSlot, id=slot_id)
        data = json.loads(request.body)
        if 'is_booked' in data:
            slot.is_booked = data['is_booked']
        if 'start_time' in data:
            slot.start_time = data['start_time']
        if 'end_time' in data:
            slot.end_time = data['end_time']
        slot.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE' and slot_id is not None:
        slot = get_object_or_404(TimeSlot, id=slot_id)
        slot.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ---------- API: Providers ----------
@csrf_exempt
def providers_api(request, provider_id=None):
    if request.method == 'GET':
        if provider_id is not None:
            provider = get_object_or_404(Provider, id=provider_id)
            data = {
                'id': provider.id,
                'username': provider.user.username,
                'specialization': provider.specialization,
            }
            return JsonResponse(data)
        providers = Provider.objects.select_related('user').all()
        data = [
            {
                'id': p.id,
                'username': p.user.username,
                'specialization': p.specialization,
            }
            for p in providers
        ]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        from django.contrib.auth.models import User
        user = User.objects.get(id=data['user_id'])
        provider = Provider.objects.create(
            user=user,
            specialization=data['specialization'],
        )
        return JsonResponse(
            {'id': provider.id, 'status': 'created'},
            status=201,
        )

    if request.method == 'PUT' and provider_id is not None:
        provider = get_object_or_404(Provider, id=provider_id)
        data = json.loads(request.body)
        if 'specialization' in data:
            provider.specialization = data['specialization']
        provider.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE' and provider_id is not None:
        provider = get_object_or_404(Provider, id=provider_id)
        provider.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ---------- API: Bookings ----------
@csrf_exempt
def bookings_api(request, booking_id=None):
    if request.method == 'GET':
        if booking_id is not None:
            booking = get_object_or_404(Booking, id=booking_id)
            data = {
                'id': booking.id,
                'client_id': booking.client_id,
                'slot_id': booking.slot_id,
                'created_at': booking.created_at.isoformat(),
            }
            return JsonResponse(data)
        bookings = Booking.objects.select_related('client', 'slot').all()
        data = [
            {
                'id': b.id,
                'client_id': b.client_id,
                'slot_id': b.slot_id,
                'created_at': b.created_at.isoformat(),
            }
            for b in bookings
        ]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        booking = Booking.objects.create(
            client_id=data['client_id'],
            slot_id=data['slot_id'],
        )
        slot = booking.slot
        slot.is_booked = True
        slot.save()
        return JsonResponse(
            {'id': booking.id, 'status': 'created'},
            status=201,
        )

    if request.method == 'PUT' and booking_id is not None:
        booking = get_object_or_404(Booking, id=booking_id)
        data = json.loads(request.body)
        old_slot = booking.slot
        if 'slot_id' in data:
            old_slot.is_booked = False
            old_slot.save()
            booking.slot_id = data['slot_id']
            new_slot = booking.slot
            new_slot.is_booked = True
            new_slot.save()
        if 'client_id' in data:
            booking.client_id = data['client_id']
        booking.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE' and booking_id is not None:
        booking = get_object_or_404(Booking, id=booking_id)
        slot = booking.slot
        slot.is_booked = False
        slot.save()
        booking.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

