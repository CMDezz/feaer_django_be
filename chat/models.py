from djongo import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    _id = models.ObjectIdField()
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person',unique=False,db_column='first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person',unique=False,db_column='second_person')
    updated = models.DateTimeField(auto_now=True,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isActive = models.BooleanField(default=True)

    objects = ThreadManager()
    class Meta:
        get_latest_by = 'updated'
        indexes = [
            models.Index(fields=['first_person', 'second_person'])
        ]
        ordering = ['-updated']


class ChatMessage(models.Model):
    _id = models.ObjectIdField()
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)