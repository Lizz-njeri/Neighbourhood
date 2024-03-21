from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# Extending User Model Using a One-To-One Link
class NeighbourHood(models.Model):
    hood_name = models.CharField(max_length=50)
    hood_logo = models.ImageField(default='default.jpg', upload_to='media/hood_logos')
    location = models.CharField(max_length=60)
    hood_admin = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='hood_admin', null=True)
    hood_description = models.TextField(null=True)
    hood_health_officer_name = models.CharField(max_length=60, null=True, blank=True)
    hood_police_officer_name = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.hood_name} hood'

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='media/profile_images')
    bio = models.TextField(max_length=254, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
   
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Business(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='business')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()

class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='hood_post')

    @classmethod
    def get_by_user(cls, user):
        posts = cls.objects.filter(user=user)
        return posts

