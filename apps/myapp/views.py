from django.shortcuts import render,redirect 
from .models import User, Trip
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
  if 'user_id' not in request.session:
    request.session['user_id'] = None
  return render(request, 'myapp/index.html')


def registration(request):
  first_name = request.POST['first_name']
  last_name = request.POST['last_name']
  email = request.POST['email']
  hash_password = bcrypt.hashpw(
      request.POST['password'].encode(), bcrypt.gensalt())

  errors = User.objects.registartion_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
      return redirect('/')
  else:
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_password)
    return redirect('/')


def login(request):
  email = request.POST['email']
  errors = User.objects.login_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
      return redirect('/')
  else:
    request.session['user_id'] = User.objects.get(email=email).id
    return redirect('/dashboard')

def dashboard(request):
  if request.session['user_id'] == None:
    return redirect('/')
  context = {
    'user_name': User.objects.get(id=request.session['user_id']).first_name,
    'trips': Trip.objects.filter(user_id=User.objects.get(id=request.session['user_id'])),
    'other_trips': Trip.objects.exclude(user_id=User.objects.get(id=request.session['user_id'])).exclude(people_joined=User.objects.get(id=request.session['user_id'])),
    'joined_trips': Trip.objects.filter(people_joined=User.objects.get(id=request.session['user_id']))
  }
  return render(request, 'myapp/dashboard.html', context)


def logout(request):
  request.session.flush()
  return redirect('/')


def create_trip(request):
  if request.session['user_id'] == None:
    return redirect('/')
  context = {
      'user_name': User.objects.get(id=request.session['user_id']).first_name
  }
  return render(request, 'myapp/create_trip.html', context)


def create_trip_cancel(request):
  return redirect('/dashboard')


def create_trip_process(request):
  destination = request.POST['destination']
  start_date = request.POST['start_date']
  end_date = request.POST['end_date']
  plan = request.POST['plan']
  errors = Trip.objects.trip_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
      return redirect('/create_trip')
  else:
    Trip.objects.create(destination=destination, start_date=start_date, end_date=end_date, plan=plan, user_id=User.objects.get(id=request.session['user_id']))
    return redirect('/dashboard')

def edit_trip(request, trip_id):
  if request.session['user_id'] == None:
    return redirect('/')
  context = {
      'user_name': User.objects.get(id=request.session['user_id']).first_name,
      'trip': Trip.objects.get(id=trip_id),
      'start_date': str(Trip.objects.get(id=trip_id).start_date),
      'end_date': str(Trip.objects.get(id=trip_id).end_date)
  }
  return render(request, 'myapp/edit_trip.html', context)


def update_trip_process(request, trip_id):
  destination = request.POST['destination']
  start_date = request.POST['start_date']
  end_date = request.POST['end_date']
  plan = request.POST['plan']
  errors = Trip.objects.trip_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
      return redirect('/edit_trip/' + str(trip_id))
  else:
    trip = Trip.objects.get(id=trip_id)
    trip.destination = destination
    trip.start_date = start_date
    trip.end_date=end_date
    trip.plan = plan
    trip.save()
    return redirect('/dashboard')


def remove_trip(request, trip_id):
  if request.session['user_id'] == None:
    return redirect('/')
  Trip.objects.get(id=trip_id).delete()
  return redirect('/dashboard')


def join_trip(request, trip_id):
  if request.session['user_id'] == None:
    return redirect('/')
  Trip.objects.get(id=trip_id).people_joined.add(User.objects.get(id=request.session['user_id']))
  return redirect('/dashboard')


def cancel_trip(request, trip_id):
  Trip.objects.get(id=trip_id).people_joined.remove(User.objects.get(id=request.session['user_id']))
  return redirect('/dashboard')


def trip_info(request, trip_id):
  context = {
    'user_name': User.objects.get(id=request.session['user_id']).first_name,
    'trip': Trip.objects.get(id=trip_id),
    'people': Trip.objects.get(id=trip_id).people_joined.all()
  }
  return render(request, 'myapp/trip_info.html', context)
