import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from workout_tracker.users.models import Profile


class Excercise(models.Model):
    PART_CHOICES = (
        ('pecs', _('pecs')),
        ('quadriceps', _('quadriceps')),
        ('glute', _('glute')),
        ('biceps', _('biceps')),
        ('triceps', _('triceps')),
        ('deltoids', _('deltoids')),
        ('lats', _('lats')),
        ('traps', _('traps')),
        ('hamstrings', _('hamstrings')),
        ('abs', _('abs'))
    )
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    primary_part = models.CharField(
        _('primary part of body'),
        choices=PART_CHOICES,
        max_length=100
    )
    secondary_part = ArrayField(
        models.CharField(max_length=10, null=True, blank=True),
    )


class LogExcercise(models.Model):
    excercise = models.ForeignKey(Excercise, on_delete=models.CASCADE)
    weights = models.FloatField()
    sets_no = models.IntegerField()
    reps_no = models.IntegerField()
    date_performed = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.excercise.name}-{self.date_performed}'


class Workout(models.Model):
    PROGRESS_CHOICES = (
        ('weights', _('weights')),
        ('reps', _('reps')),
        ('sets', _('sets'))
    )
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    repeated_no = models.IntegerField(default=0)
    max_repeat_no = models.IntegerField(default=2)
    progress_choice = models.CharField(
        _('what to do for the next set'),
        choices=PROGRESS_CHOICES,
        max_length=100,
        null=True, blank=True
    )
    sets_no = models.IntegerField()
    reps_no = models.IntegerField()
    break_time_length = models.TimeField(default=datetime.time(0, 1, 30))

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WorkoutSet(Workout):
    weights = models.FloatField()


class SuperSet(Workout):
    workout_sets = models.ManyToManyField(WorkoutSet)


class Program(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    worktout_sets = models.ManyToManyField(WorkoutSet)
    super_sets = models.ManyToManyField(SuperSet)
    repeated_no = models.IntegerField(default=0)
    date_performed = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
