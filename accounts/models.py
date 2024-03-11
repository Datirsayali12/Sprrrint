from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    user_image = models.URLField()
    is_pro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class BillingPersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    
class UserSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    preference = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)

    def __str__(self):
        return f"Selection for User: {self.user.username}"