from django.shortcuts import render, redirect
from artist.models import Artist, Announcements, Tour
from fan.models import Fan
import bcrypt
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse

def index(request):
    return render(request, "index.html")

def register_fan(request):
    errors = Fan.objects.fan_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Fan.objects.create(
            username = request.POST['username'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard/fan/')

def register_artist(request):
    errors = Artist.objects.artist_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Artist.objects.create(
            stage_name = request.POST['stage_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard/artist/')

def login(request):
    if request.method == 'POST':
        email_id = request.POST['email']
        if Artist.objects.filter(email=email_id).exists():
            print("User is Artist")
            user = Artist.objects.filter(email=email_id)
            if len(user) > 0:
                user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('/dashboard/artist/')
        else:
            print("User is Fan")
            user = Fan.objects.filter(email=email_id)
            if len(user) > 0:
                user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('/dashboard/fan/')

def dashboard_artist(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    user = Artist.objects.get(id = request.session['user_id'])
    fans = user.followed_by.all()
    shows = Tour.objects.filter(tour_added_by=user)
    shows_count = Tour.objects.filter(tour_added_by=user).count()
    rsvps = (Tour.objects.annotate(attendees=Count('attendee')).filter(tour_added_by=user, attendees__gt=0))
    posted_announcements = Announcements.objects.filter(ann_posted_by=user)
    new_tour_date = Tour.objects.last()
    context = {
        'user': user,
        'posted_announcements': posted_announcements,
        'fans': fans,
        'posted_tour_date': shows,
        'shows': shows,
        'rsvps': rsvps,
        'new_tour_date': new_tour_date
    }
    return render(request, "artist/index.html", context)

def dashboard_fan(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    user = Fan.objects.get(id = request.session['user_id'])
    fans_artists = Artist.objects.filter(followed_by=user)
    fans_shows = Tour.objects.filter(attendee=user)
    artists_count = Artist.objects.filter(followed_by=user).count()
    show_count = Tour.objects.filter(attendee=user).count()
    followed_anns = Announcements.objects.filter(ann_posted_by__in=fans_artists)
    stars_to_go = 5 - show_count
    if show_count > 5:
        rewards = range(0, 5)
    else:
        rewards = range(0, show_count)
    context = {
        'user': user,
        'followed_anns': followed_anns,
        'fans_artists': fans_artists,
        'fans_shows': fans_shows,
        'followed_artists': artists_count,
        'shows_attending': show_count,
        'rewards': rewards,
        'stars_to_go': range(0, stars_to_go),
    }
    return render(request, "fan/index.html", context)

def all_artists(request):
    context = {
        'user': Fan.objects.get(id = request.session['user_id']),
        'all_artists': Artist.objects.all(),
    }
    return render(request, "artists.html", context)

def artist_profile(request, artist_id):
    context = {
        'user': Fan.objects.get(id = request.session['user_id']),
        'artist': Artist.objects.get(id = artist_id),
        'posted_announcements': Announcements.objects.filter(ann_posted_by=artist_id),
        'posted_tour_date': Tour.objects.filter(tour_added_by=artist_id)
    }
    return render(request, "profile.html", context)

def rsvp(request, artist_id, tour_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    data = {}
    if request.method == "POST":
        user = Fan.objects.get(id = request.session['user_id'])
        show = Tour.objects.get(id = tour_id)
        if user.rsvp_by.filter(id=show.id).exists():
            attending = False
            user.rsvp_by.remove(show)
        else: 
            user.rsvp_by.add(show)
            attending = True
    data["attending"] = attending
    return JsonResponse(data)

def cancel(request, artist_id, tour_id):
    data = {}
    user = Fan.objects.get(id = request.session['user_id'])
    show = Tour.objects.get(id = tour_id)
    user.rsvp_by.remove(show)
    cancel = True
    data["cancel"] = cancel
    return JsonResponse(data)

def logout(request):
    request.session.flush()
    return redirect('/')