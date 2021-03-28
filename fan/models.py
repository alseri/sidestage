from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]*$')

class FanManager(models.Manager):
    def fan_validator(self, post_data):
        fan_errors = {}
        if len(post_data['username']) < 1:
            fan_errors['username'] = "USERNAME must be at least 1 character."
        if not USERNAME_REGEX.match(post_data['username']):
            fan_errors['username'] = "USERNAME cannot include spaces."  
        if not EMAIL_REGEX.match(post_data['email']):
            fan_errors['email'] = "EMAIL must be valid format."
        if len(post_data['password']) < 8:
            fan_errors['password'] = "PASSWORD must be at least 8 characters."
        if post_data['password'] != post_data['cpassword']:
            fan_errors['cpassword'] = "PASSWORDS do not match."
        return fan_errors

class Fan(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    rewards = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FanManager()