from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import TA, Course, TutoringHour
from .forms import TASignupForm, TutoringHourForm
from datetime import datetime, date

def home(request):
    """Public homepage showing all tutoring hours"""
    tutoring_hours = TutoringHour.objects.select_related('ta', 'ta__user').prefetch_related('ta__courses').all()

    # Filter out expired hours
    today = date.today()
    active_hours = []
    for hour in tutoring_hours:
        if hour.until_date is None or hour.until_date >= today:
            active_hours.append(hour)

    # Organize by day of week
    hours_by_day = {}
    for i in range(7):
        day_name = dict(TutoringHour.DAYS_OF_WEEK)[i]
        hours_by_day[day_name] = [h for h in active_hours if h.day_of_week == i]

    # Organize by course
    courses = Course.objects.all()
    hours_by_course = {}
    for course in courses:
        course_hours = [h for h in active_hours if course in h.ta.courses.all()]
        if course_hours:
            hours_by_course[course] = course_hours

    context = {
        'hours_by_day': hours_by_day,
        'hours_by_course': hours_by_course,
        'all_hours': active_hours,
    }
    return render(request, 'tutor_scheduler/home.html', context)

def ta_detail(request, ta_id):
    """Detail page for a specific TA"""
    ta = get_object_or_404(TA, id=ta_id)
    today = date.today()

    # Filter active hours
    active_hours = [h for h in ta.tutoring_hours.all()
                   if h.until_date is None or h.until_date >= today]

    context = {
        'ta': ta,
        'active_hours': active_hours,
    }
    return render(request, 'tutor_scheduler/ta_detail.html', context)

def ta_signup(request):
    """TA signup page"""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        ta_form = TASignupForm(request.POST)

        if user_form.is_valid() and ta_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()

            ta = ta_form.save(commit=False)
            ta.user = user
            ta.save()
            ta_form.save_m2m()  # Save many-to-many relationships

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('ta_dashboard')
    else:
        user_form = UserCreationForm()
        ta_form = TASignupForm()

    context = {
        'user_form': user_form,
        'ta_form': ta_form,
    }
    return render(request, 'tutor_scheduler/ta_signup.html', context)

def ta_login(request):
    """TA login page"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ta_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'tutor_scheduler/ta_login.html', {'form': form})

@login_required
def ta_logout(request):
    """TA logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def ta_dashboard(request):
    """TA dashboard to manage tutoring hours"""
    try:
        ta = request.user.ta
    except TA.DoesNotExist:
        messages.error(request, 'You do not have a TA profile.')
        return redirect('home')

    today = date.today()
    active_hours = [h for h in ta.tutoring_hours.all()
                   if h.until_date is None or h.until_date >= today]

    context = {
        'ta': ta,
        'active_hours': active_hours,
    }
    return render(request, 'tutor_scheduler/ta_dashboard.html', context)

@login_required
def add_tutoring_hour(request):
    """Add a new tutoring hour"""
    try:
        ta = request.user.ta
    except TA.DoesNotExist:
        messages.error(request, 'You do not have a TA profile.')
        return redirect('home')

    if request.method == 'POST':
        form = TutoringHourForm(request.POST)
        if form.is_valid():
            hour = form.save(commit=False)
            hour.ta = ta
            hour.save()
            messages.success(request, 'Tutoring hour added successfully!')
            return redirect('ta_dashboard')
    else:
        form = TutoringHourForm()

    return render(request, 'tutor_scheduler/add_hour.html', {'form': form})

@login_required
def edit_tutoring_hour(request, hour_id):
    """Edit an existing tutoring hour"""
    try:
        ta = request.user.ta
    except TA.DoesNotExist:
        messages.error(request, 'You do not have a TA profile.')
        return redirect('home')

    hour = get_object_or_404(TutoringHour, id=hour_id, ta=ta)

    if request.method == 'POST':
        form = TutoringHourForm(request.POST, instance=hour)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutoring hour updated successfully!')
            return redirect('ta_dashboard')
    else:
        form = TutoringHourForm(instance=hour)

    return render(request, 'tutor_scheduler/edit_hour.html', {'form': form, 'hour': hour})

@login_required
def delete_tutoring_hour(request, hour_id):
    """Delete a tutoring hour"""
    try:
        ta = request.user.ta
    except TA.DoesNotExist:
        messages.error(request, 'You do not have a TA profile.')
        return redirect('home')

    hour = get_object_or_404(TutoringHour, id=hour_id, ta=ta)

    if request.method == 'POST':
        hour.delete()
        messages.success(request, 'Tutoring hour deleted successfully!')
        return redirect('ta_dashboard')

    return render(request, 'tutor_scheduler/delete_hour.html', {'hour': hour})
