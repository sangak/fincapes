from django.db import models
from django.db.models.signals import pre_save
from fincapes.utils import unique_id_generator


class SubscriberQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by('-timestamp')


class SubscriberManager(models.Manager):
    def get_queryset(self):
        return SubscriberQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent()

    def get_by_pk(self, pk):
        qs = self.all().filter(pk=pk)
        if qs.exists():
            return qs.first()
        return None


class Subscriber(models.Model):
    uid = models.CharField(max_length=64, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subscriber_types = models.CharField(max_length=125, blank=True, default='newsletter')

    objects = SubscriberManager()

    def __str__(self):
        return self.email


def pre_save_subscriber_create(sender, instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_subscriber_create, sender=Subscriber)