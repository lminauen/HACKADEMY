from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional attributes you want
    postalCode = models.IntegerField()
    street = models.CharField(max_length=150)
    language = models.CharField(choices=(('de', 'German'),
                                         ('fr', 'French'),
                                         ('it', 'Italian'),
                                         ('en', 'English')),
                                default='de',
                                max_length=50)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username


class community(models.Model):
    postalCode = models.IntegerField()
    name = models.CharField(max_length=100)


class type(models.Model):
    name = models.CharField(choices=(('defib', 'Defibrillator'),
                                     ('sos', 'SOS Telephone')),
                            default='defib',
                            max_length=100)


class items(models.Model):
    user = models.ForeignKey(UserProfileInfo, related_name="users", on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(type, related_name="type", on_delete=models.CASCADE)
    community = models.ForeignKey(community, related_name="community", on_delete=models.CASCADE)
    longitude = models.DecimalField(decimal_places=10, max_digits=12)
    latitude = models.DecimalField(decimal_places=10, max_digits=12)
    availability = models.CharField(max_length=300, null=True, blank=True)


class defibModels(models.Model):
    name = models.CharField(max_length=100)
    modelNr = models.IntegerField()
    automatic = models.BooleanField(default=False)
    guided = models.BooleanField(default=False)
    compression = models.BooleanField(default=False)


class attributesDefib(models.Model):
    item = models.ForeignKey(items, related_name="users", on_delete=models.CASCADE)
    model = models.ForeignKey(defibModels, related_name="defibModels", on_delete=models.CASCADE)
