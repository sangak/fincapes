from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from fincapes.utils import unique_id_generator
from ..models import Project

User = get_user_model()


class UltimateOutcome(models.Model):
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL, related_name='logic_model')
    uid = models.CharField(max_length=64, unique=True, editable=False)
    code = models.SmallIntegerField(unique=True, default=1000)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ulti_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ulti_modified')

    class Meta:
        verbose_name_plural = 'Ultimate Outcome'

    def __str__(self):
        return self.description


def pre_save_ultimate_outcome(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_ultimate_outcome, sender=UltimateOutcome)


class IntermediateOutcomeQueryset(models.query.QuerySet):
    def recent(self):
        return self.order_by('code')


class IntermediateOutcomeManager(models.Manager):
    def get_queryset(self):
        return IntermediateOutcomeQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent()

    def new_code(self):
        parent = UltimateOutcome.objects.first()
        max_code = self.all().aggregate(Max('code'))['code__max']
        return int(parent.code) + int(max_code) + 100

    def all(self):
        return self.get_queryset().recent().all()


class IntermediateOutcome(models.Model):
    ulti_outcome = models.ForeignKey(UltimateOutcome, null=True, on_delete=models.CASCADE, related_name='inter_outcomes')
    uid = models.CharField(max_length=64, unique=True, editable=False)
    code = models.SmallIntegerField(unique=True, null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inter_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inter_modified')

    objects = IntermediateOutcomeManager()

    def __str__(self):
        return self.description


def pre_save_intermediate_outcome(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_intermediate_outcome, sender=IntermediateOutcome)


class ImmediateOutcomeQueryset(models.query.QuerySet):
    def recent(self):
        return self.order_by('code')


class ImmediateOutcomeManager(models.Manager):
    def get_queryset(self):
        return ImmediateOutcomeQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent()

    def new_code(self, parent_uid=None):
        parent = IntermediateOutcome.objects.filter(uid=parent_uid)
        if parent.exists():
            parent.first()
            max_code = self.all().aggregate(Max('code'))['code__max']
            return int(parent.code) + int(max_code) + 10
        return None


class ImmediateOutcome(models.Model):
    inter_outcome = models.ForeignKey(IntermediateOutcome, null=True, on_delete=models.CASCADE, related_name='imme_outcomes')
    uid = models.CharField(max_length=64, unique=True, editable=False)
    code = models.SmallIntegerField(unique=True, null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='imme_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='imme_modified')

    objects = ImmediateOutcomeManager()

    def __str__(self):
        return self.description


def pre_save_immediate_outcome(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_immediate_outcome, sender=ImmediateOutcome)


class OutputQueryset(models.query.QuerySet):
    def recent(self):
        return self.order_by('code')


class OutputManager(models.Manager):
    def get_queryset(self):
        return OutputQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().recent()

    def new_code(self, uid=None):
        parent = ImmediateOutcome.objects.filter(uid=uid)
        if parent.exists():
            parent.first()
            max_code = self.all().aggregate(Max('code'))['code__max']
            return int(parent.code) + int(max_code) + 1
        return None


class Output(models.Model):
    imme_outcome = models.ForeignKey(ImmediateOutcome, null=True, on_delete=models.CASCADE, related_name='outputs')
    uid = models.CharField(max_length=64, unique=True, editable=False)
    code = models.SmallIntegerField(unique=True, null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='output_added')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='output_modified')

    objects = OutputQueryset()

    def __str__(self):
        return self.description


def pre_save_output(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_output, sender=Output)