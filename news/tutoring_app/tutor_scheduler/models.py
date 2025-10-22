from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Represents a course that can be tutored (e.g., CSCI 150, CSCI 151)"""
    code = models.CharField(max_length=20, unique=True)  # e.g., "CSCI 150"
    name = models.CharField(max_length=200, blank=True)  # e.g., "Introduction to Programming"

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class TA(models.Model):
    """Represents a Teaching Assistant"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    courses = models.ManyToManyField(Course, related_name='tas', blank=True)

    class Meta:
        verbose_name = 'TA'
        verbose_name_plural = 'TAs'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TutoringHour(models.Model):
    """Represents tutoring availability for a TA"""
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    ta = models.ForeignKey(TA, on_delete=models.CASCADE, related_name='tutoring_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    until_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.ta} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
