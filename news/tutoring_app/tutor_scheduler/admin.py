from django.contrib import admin
from .models import Course, TA, TutoringHour

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(TA)
class TAAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'major', 'user']
    list_filter = ['major', 'courses']
    search_fields = ['user__first_name', 'user__last_name', 'major']
    filter_horizontal = ['courses']

@admin.register(TutoringHour)
class TutoringHourAdmin(admin.ModelAdmin):
    list_display = ['ta', 'get_day_of_week_display', 'start_time', 'end_time', 'is_recurring', 'until_date']
    list_filter = ['day_of_week', 'is_recurring', 'ta']
    search_fields = ['ta__user__first_name', 'ta__user__last_name']
