from django.db import models
from django.contrib.auth.models import User

class ProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='Profile_pic',null=True)
    bio=models.TextField(null=True)
    phone=models.IntegerField(null=True)

class Property(models.Model):
    CATEGORY_CHOICES = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
        ('Hybrid', 'Hybrid'),
    ]
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Sale'
    )
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='property_images', null=True, blank=True)
    saved_users = models.ManyToManyField(User, related_name='saved_properties', blank=True)
    user = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    @property
    def total_post(self):
        return Property.objects.filter(user=self.user).count()
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
