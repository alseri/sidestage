from django.db import models 
import re
from fan.models import Fan

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ArtistManager(models.Manager):
    def artist_validator(self, post_data):
        artist_errors = {}
        if len(post_data['stage_name']) < 1:
            artist_errors['stage_name'] = "STAGE NAME is required."
        if not EMAIL_REGEX.match(post_data['email']):
            artist_errors['email'] = "EMAIL must be valid format."
        if len(post_data['password']) < 8:
            artist_errors['password'] = "PASSWORD must be at least 8 characters."
        if post_data['password'] != post_data['cpassword']:
            artist_errors['cpassword'] = "PASSWORDS do not match."
        return artist_errors

class Artist(models.Model):
    email = models.CharField(max_length=255)
    stage_name = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    hometown = models.CharField(null=True, max_length=255)
    genre = models.CharField(null=True, max_length=100)
    website = models.CharField(null=True, max_length=255)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    bio = models.TextField(null=True)
    followed_by = models.ManyToManyField(Fan, related_name = "artist_followed_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ArtistManager()

class Announcements(models.Model):
    ann_post = models.TextField()
    ann_posted_by = models.ForeignKey(Artist, related_name="ann_added", null=True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(Fan, related_name = "liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TourManager(models.Manager):
    def tour_validator(self, post_data):
        tour_errors = {}
        if len(post_data['tour_location']) < 1:
            tour_errors['tour_location'] = "SHOW LOCATION is required."
        if len(post_data['tour_venue']) < 1:
            tour_errors['tour_venue'] = "SHOW VENUE is required."
        if len(post_data['tour_date']) < 1:
            tour_errors['tour_date'] = "SHOW DATE is required."
        if len(post_data['tour_time']) < 1:
            tour_errors['tour_time'] = "SHOW TIME is required."
        if len(post_data['tour_price']) < 1:
            tour_errors['tour_price'] = "SHOW PRICE is required."

        return tour_errors


class Tour(models.Model):
    location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    show_date = models.DateTimeField(null=True)
    show_time = models.TimeField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    tickets = models.TextField(null=True)
    details = models.CharField(max_length=255, null=True)
    tour_added_by = models.ForeignKey(Artist, related_name="tour_added", null=True, on_delete = models.CASCADE)
    attendee = models.ManyToManyField(Fan, related_name = "rsvp_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TourManager()