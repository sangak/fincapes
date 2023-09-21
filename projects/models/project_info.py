from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from donors.models import Donor
from fincapes.helpers import get_locale_date
from fincapes.utils import unique_id_generator, unique_slug_generator, currency, get_time_diff
from fincapes.variables import CURRENCY_CHOICES

User = get_user_model()


class ProjectQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1).order_by('title')

    def recent(self):
        return self.order_by('title')


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def get_by_pk(self, pk):
        qs = self.get_queryset().recent().filter(pk=pk)
        if qs.exists():
            return qs.first()
        return None

    def all(self):
        return self.get_queryset().recent()


class Project(models.Model):
    uid = models.CharField(max_length=64, unique=True, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    acronym = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    brief_description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='added_project', null=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='modified_project', null=True)

    objects = ProjectManager()

    def __str__(self):
        return self.title

    # @property
    def get_local_project_start(self, bhs=None):
        start = self.date_start
        return get_locale_date(start, bhs=bhs)

    # @property
    def get_local_project_end(self, bhs=None):
        end = self.date_end
        return get_locale_date(end, bhs=bhs)

    @property
    def get_period_years(self):
        years = get_time_diff(self, interval='years')
        start = self.date_start.year
        end_ = self.date_end.year
        period = [start + i for i in range(years)]
        year_list = [str(x) for x in period]
        if not end_ in year_list:
            year_list.append(end_)
        return year_list

    @property
    def total_amount(self):
        uid = self.uid
        total = Commitment.objects.filter(project__uid=uid).aggregate(Sum('amount'))
        return currency(total.get('amount__sum'))


def pre_save_project(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)

    if instance.title:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_project, sender=Project)


class Commitment(models.Model):
    uid = models.CharField(max_length=64, unique=True, null=True, blank=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_commitment', null=True, blank=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donor_commitment', null=True, blank=True)
    currency = models.SmallIntegerField(choices=CURRENCY_CHOICES, default=1)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.project.acronym}" if self.project is not None else self.uid

    @property
    def get_project(self):
        return self.project.acronym

    @property
    def get_donor(self):
        return self.donor.acronym

    @property
    def total_amount(self):
        return currency(self.amount)


def pre_save_commitment(instance, *args, **kwargs):
    if not instance.uid:
        instance.uid = unique_id_generator(instance)


pre_save.connect(pre_save_commitment, sender=Commitment)