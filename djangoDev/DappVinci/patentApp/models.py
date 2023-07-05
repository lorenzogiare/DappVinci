from django.db import models
from django.conf import settings
from django.forms import BooleanField
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from djongo.models.fields import ObjectIdField, EmbeddedField, ArrayField
from django.db.models.signals import post_save


# -------------- SUB-MODELS -------------------------------------------------------------
# sub-model for patents field in Account model
class PatentIds(models.Model):
    patentId = models.IntegerField()
    _id = ObjectIdField()


# sub-model for depositInfo field in PatentContent Model
class DepositInfo(models.Model):
    _id = ObjectIdField()
    currentAssignee = models.CharField(max_length=20)
    applicationDate = models.DateTimeField(default=timezone.now, editable=False)
    inventors = models.CharField(max_length=40)


# sub-model for logs field in Event model
class EventLogs(models.Model):
    _id = ObjectIdField()
    arg1 = models.CharField(max_length=20)
    arg2 = models.CharField(max_length=20)
    arg3 = models.CharField(max_length=20)

# -------------------------------- MAIN MODELS ----------------------------------------------- 
# model for the content of a Patent
class PatentContent(models.Model):
    hash = models.CharField(max_length=100)
    title = models.CharField(max_length=40)
    sector = models.CharField(max_length=20)
    introduction = models.CharField(max_length=100)
    description = models.TextField()
    claims = models.TextField()
    image = models.FileField(upload_to='images/')   # uploads to MEDIA_ROOT/images/
    depositInfo = EmbeddedField(model_container=DepositInfo)
    _id = ObjectIdField()    

# model of a Patent
class Patent(models.Model):
    title = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = EmbeddedField(model_container=PatentContent)


# model for events emitted from the blockchain
EVENTS = [
    ("newPatent", "patent created"),
    ("modPatent", "patent changed"),
]

class Event(models.Model):
    _id = ObjectIdField()
    patentId = models.IntegerField()
    type = models.CharField(max_length=20, choices=EVENTS)
    logs = ArrayField(model_container=EventLogs)


 #-----EXSTENSION-OF-THE-USER-MODEL----------------------------------------------------
# model for extension of User model
class Account(models.Model):
    _id = ObjectIdField()
    address = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patents = ArrayField(model_container=PatentIds)

    def __str__(self):
        return self.user.username

#when a new User object is created, the Profile model is too
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()
