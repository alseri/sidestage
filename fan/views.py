from django.shortcuts import render, redirect
from artist.models import Artist, Tour, Announcements
from fan.models import Fan
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    return render(request, "fan/index.html")

def show_new_show_count_fan(request):
    user = Fan.objects.get(id = request.session['user_id'])
    shows_count = Tour.objects.filter(attendee=user).count()
    context = {
        'shows_count': shows_count,
    }
    return render(request, 'fan/partials/tours/show_count.html', context)

def like_ann(request, ann_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    data = {}
    if request.method == "POST":
        user = Fan.objects.get(id = request.session['user_id'])
        ann = Announcements.objects.get(id = ann_id)
        if user.liked_by.filter(id=ann.id).exists():
            like = False
            user.liked_by.remove(ann)
        else:
            user.liked_by.add(ann)
            like = True
    data["liked"] = like
    return JsonResponse(data)

def follow_artist(request, artist_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    data = {}
    if request.method == "POST":
        user = Fan.objects.get(id = request.session['user_id'])
        artist = Artist.objects.get(id = artist_id)
        if user.artist_followed_by.filter(id=artist.id).exists():
            follow = False
            user.artist_followed_by.remove(artist)
        else:
            user.artist_followed_by.add(artist)
            follow = True
    data["followed"] = follow
    return JsonResponse(data)

def rewards_refresh(request):
    user = Fan.objects.get(id = request.session['user_id'])
    show_count = Tour.objects.filter(attendee=user).count()
    stars_to_go = 5 - show_count
    if show_count > 5:
        rewards = range(0, 5)
    else:
        rewards = range(0, show_count)
    context = {
        'rewards': rewards,
        'stars_to_go': range(0, stars_to_go),
    }
    return render(request, 'fan/partials/rewards/rewards.html', context)