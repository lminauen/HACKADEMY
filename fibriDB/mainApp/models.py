from django.db import models

# Create your models here.


class community(models.Model):
    postalCode = models.IntegerField()
    name = models.CharField(max_length=100)


class items(models.Model):
    # user = models.ForeignKey(user, related_name="users", on_delete=models.CASCADE)
    type = models.ForeignKey(type, related_narelated_name="type", on_delete=models.CASCADE)
    community = models.ForeignKey(community, related_narelated_name="community", on_delete=models.CASCADE)
    longitude = models.DecimalField(decimal_places=10, max_digits=12)
    latitude = models.DecimalField(decimal_places=10, max_digits=12)


class type(models.Model):
    name = models.CharField(choices=(('defib', 'Defibrillator'),
                                     ('sos', 'SOS Telephone')),
                            default='defib',
                            max_length=100)


class defibModels(models.Model):
    name = models.CharField(max_length=100)
    modelNr = models.IntegerField()
    automatic = models.BooleanField(default=False)
    guided = models.BooleanField(default=False)
    compression = models.BooleanField(default=False)


class attributesDefib(models.Model):
    item = models.ForeignKey(items, related_name="users", on_delete=models.CASCADE)
    model = models.ForeignKey(defibModels, related_name="defibModels", on_delete=models.CASCADE)
