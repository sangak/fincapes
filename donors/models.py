from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.urls import reverse
from fincapes.utils import unique_id_generator, unique_slug_generator
from fincapes.variables import DONOR_STATUS_CHOICES

User = get_user_model()


class DonorQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1).order_by('title')

    def recent(self):
        return self.order_by('title')


class DonorManager(models.Manager):
    def get_queryset(self):
        return DonorQuerySet(self.model, using=self._db)

    def get_by_pk(self, pk):
        qs = self.get_queryset().recent().filter(pk=pk)
        if qs.exists():
            return qs.first()
        return None

    def active(self):
        return self.get_queryset().active()

    def all(self):
        return self.get_queryset().recent().all()


class Donor(models.Model):
    uid = models.CharField(max_length=64, unique=True, editable=False)
    title = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True)
    acronym = models.CharField(max_length=30, blank=True, null=True)
    status = models.SmallIntegerField(default=0, choices=DONOR_STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='added_donor', null=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='modified_donor', null=True)

    objects = DonorManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('donor:detail', kwargs={'uid': self.uid})


def pre_save_donor(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)

    if instance.title:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_donor, sender=Donor)