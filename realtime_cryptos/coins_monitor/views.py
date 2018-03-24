from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import CoinMonitor
from . import pusher

@login_required
def generic_team(request):
    if not request.user.coinmonitor_set.exists():
        return HttpResponse("You haven't been granted a CoinMonitor team yet")
    coin_monitor = request.user.coinmonitor_set.last()
    return redirect(reverse('team', kwargs={
        'symbol': coin_monitor.symbol.lower()
    }))


@login_required
def team(request, symbol):
    try:
        monitor_team = CoinMonitor.objects.get(
            symbol=symbol.upper(), monitors__id=request.user.id)
    except CoinMonitor.DoesNotExist:
        return redirect(reverse('generic_team'))

    # return HttpResponse("Hola {}".format(monitor_team.symbol))
    return render(request, 'team.html', {
        'monitor_team': monitor_team
    })


def index(request):
    return render(request, 'index.html')


def pusher_auth(request):
    pusher_client = pusher.connect()
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    prefix = 'presence-channel-'
    if not request.POST['channel_name'].startswith(prefix):
        # We're handling only presence channels for now
        return HttpResponseForbidden()

    print(request.POST)
    _, symbol = request.POST['channel_name'].split(prefix)

    is_team_member = CoinMonitor.objects.filter(
        symbol__iexact=symbol, monitors__id=request.user.id).exists()
    if not is_team_member:
        return HttpResponseForbidden()
    kwargs = {
        'channel': request.POST['channel_name'],
        'socket_id': request.POST['socket_id'],
    }

    if request.POST['channel_name'].startswith(prefix):
        kwargs['custom_data'] = {
            'user_id': request.user.id,
            'user_info': {
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'full_name': request.user.get_full_name()
            }
        }

    auth = pusher_client.authenticate(**kwargs)
    return JsonResponse(auth)
