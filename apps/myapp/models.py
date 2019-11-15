from django.db import models
import re
import bcrypt
from datetime import datetime, date
import datetime


class UserManager(models.Manager):
  def registartion_validator(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
      errors['first_name'] = 'First and last name should be at least 2 characters long'
    if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
      errors['first_name'] = 'Name should contain only letters'
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Invalid email address!"
    if len(postData['password']) < 8:
      errors['password'] = 'Password should be at least 8 characters long'
    if postData['password'] != postData['confirm_password']:
      errors['password'] = 'Provided passwords do not match'
    if len(User.objects.filter(email=postData['email'])) != 0:
      errors['email'] = 'This email is already registered'
    return errors

  def login_validator(self, postData):
    errors = {}
    if len(User.objects.filter(email=postData['email'])) == 0:
      errors['email'] = 'This email is not registered'
    elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()):
      errors['password'] = 'Incorrect password'
    return errors


class TripManager(models.Manager):
  def trip_validator(self, postData):
    errors = {}
    destination = postData['destination'].replace(" ", "")
    today_date = datetime.datetime.today()
    start_date = datetime.datetime.strptime(postData['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(postData['end_date'], '%Y-%m-%d')
    if len(postData['destination']) == 0:
      errors['destination'] = 'Provide destination'
    elif len(postData['destination']) < 3:
      errors['destination'] = 'Destination should be at leats 3 letter long'
    elif len(postData['start_date']) == 0:
      errors['destination'] = 'Provide start date'
    elif len(postData['end_date']) == 0:
      errors['destination'] = 'Provide end date'
    elif not destination.isalpha():
      errors['destination'] = 'Destination must contain letters only'
    # *******************checking date*************************
    if start_date < today_date:
      errors['start_date'] = 'Start date cant be past'
    if end_date < start_date:
      errors['start_date'] = 'End date should be after start date'
    # *******************checking date*************************
    return errors
    


class User(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.CharField(max_length=45)
  password = models.CharField(max_length=65)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __repr__(self):
    return f"{self.email} {self.password}"

class Trip(models.Model):
  destination = models.CharField(max_length=30)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  plan = models.TextField(default='No plan yet...')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user_id = models.ForeignKey(User, related_name="trips")
  people_joined = models.ManyToManyField(User, related_name="people_on_trip")
  objects = TripManager()

