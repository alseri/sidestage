from django.shortcuts import render, redirect
from artist.models import Tour, Artist, Announcements
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')

def show_new_show(request):
    user = Artist.objects.get(id = request.session['user_id'])
    posted_tour_date = Tour.objects.filter(tour_added_by=user)
    context = {
        'posted_tour_date': posted_tour_date,
    }
    return render(request, 'artist/partials/tours/new_show.html', context)

def show_new_show_count(request):
    user = Artist.objects.get(id = request.session['user_id'])
    shows_count = Tour.objects.filter(tour_added_by=user).count()
    context = {
        'shows_count': shows_count,
    }
    return render(request, 'artist/partials/tours/show_count.html', context)

def show_new_ann(request):
    user = Artist.objects.get(id = request.session['user_id'])
    posted_announcements = Announcements.objects.filter(ann_posted_by=user)
    context = {
        'posted_announcements': posted_announcements,
    }
    return render(request, 'artist/partials/anns/new_ann.html', context)

def add_ann(request):
    data = {}
    if request.method == "POST":
        if 'user_id' in request.session:
            user = Artist.objects.get(id = request.session['user_id'])
            new_ann = Announcements.objects.create(
                ann_post = request.POST['ann_post'],
                ann_posted_by = user
            )
            submitted = True
            data["submitted"] = submitted
        return JsonResponse(data)

def delete_ann(request, ann_id):
    data = {}
    ann = Announcements.objects.get(id = ann_id)
    ann.delete()
    deletion = True
    data["deletion"] = deletion
    return JsonResponse(data)

def add_tour(request):
    data = {}
    errors = Tour.objects.tour_validator(request.POST)
    if len(errors) > 0:
        print("Form errors")
        for k, v in errors.items():
            messages.error(request, v)
        return JsonResponse(errors)
    else:
        if request.method == "POST":
            if 'user_id' in request.session:
                user = Artist.objects.get(id = request.session['user_id'])
                new_tour = Tour.objects.create(
                    location = request.POST['tour_location'],
                    venue = request.POST['tour_venue'],
                    show_date = request.POST['tour_date'],
                    show_time = request.POST['tour_time'],
                    price = request.POST['tour_price'],
                    tickets = request.POST['tour_ticket'],
                    details = request.POST['tour_details'],
                    tour_added_by = user
                )
                submitted = True
                data["submitted"] = submitted
            return JsonResponse(data)

def delete_tour(request, tour_id):
    data = {}
    tour = Tour.objects.get(id = tour_id)
    tour.delete()
    deletion = True
    data["deletion"] = deletion
    return JsonResponse(data)

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to access Sidestage.")
        return redirect('/')
    context = {
        'user': Artist.objects.get(id = request.session['user_id']),
    }
    return render(request, "artist/profile.html", context)

def edit_profile(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            user = Artist.objects.get(id = request.session['user_id'])
            user.stage_name = request.POST['stage_name']
            user.hometown = request.POST['hometown']
            user.genre = request.POST['genre']
            user.website = request.POST['website']
            user.bio = request.POST['bio']
            user.save()
            return redirect('/dashboard/artist/')