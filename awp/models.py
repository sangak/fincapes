from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from projects.models import Output
from fincapes.utils import unique_id_generator
from fincapes import variables

User = get_user_model()


class SubActivityQueryset(models.query.QuerySet):
    def recent(self):
        return self.order_by('timestamp')


class SubActivityManager(models.Manager):
    def get_queryset(self):
        return SubActivityQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent().all()


class SubActivity(models.Model):
    uid = models.CharField(max_length=64, unique=True, editable=False)
    sorted_str = models.CharField(max_length=1, choices=variables.CHOICES_STR, null=True, blank=True)
    title = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='awp_sub_activity_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='awp_sub_activity_modified')

    objects = SubActivityManager()

    def __str__(self):
        return self.title


class AwpQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by('timestamp')


class AwpManager(models.Manager):
    def get_queryset(self):
        return AwpQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent()

    def new_num(self, output=None):
        qs = self.all().filter(output=output)
        if qs.count() > 0:
            num = qs.aggregate(Max('sorted_num'))['sorted_num__max']
            return int(num) + 1
        return 1


class Awp(models.Model):
    output = models.ForeignKey(Output, on_delete=models.DO_NOTHING, null=True, related_name='awp')
    uid = models.CharField(max_length=64, unique=True, editable=False)
    sorted_num = models.SmallIntegerField(null=True, blank=True)
    title = models.TextField(null=True)
    sub_activity = models.ManyToManyField(SubActivity, related_name='awp_output')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='awp_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='awp_modified')

    objects = AwpManager()

    def __str__(self):
        return self.title


def pre_save_awp(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_awp, sender=Awp)