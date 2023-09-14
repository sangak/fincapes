from django.contrib import admin
from .models import (
    Project, Commitment, UltimateOutcome, IntermediateOutcome,
    ImmediateOutcome, Output)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['acronym', 'title']


class UltimateAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']


admin.site.register(Project, ProjectAdmin)


class CommitmentAdmin(admin.ModelAdmin):
    list_display = ['get_donor', 'total_amount']


admin.site.register(Commitment, CommitmentAdmin)
admin.site.register(UltimateOutcome, UltimateAdmin)


class IntermediateAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    ordering = ['code']


admin.site.register(IntermediateOutcome, IntermediateAdmin)


class ImmediateAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    ordering = ['code']


admin.site.register(ImmediateOutcome, ImmediateAdmin)


class OutputAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    ordering = ['code']


admin.site.register(Output, OutputAdmin)