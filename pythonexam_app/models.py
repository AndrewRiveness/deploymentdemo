from django.db import models
import bcrypt
import re 
from datetime import date

class UserManager(models.Manager):
	def registrationValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		userswithmatchingemail = User.objects.filter(email = postData['UserEmail'])
		errors = {}
		if len(postData['UserFirst']) == 0:
			errors['UserFirst'] = "First Name is required"
		if len(postData['UserLast']) == 0:
			errors['UserLast'] = "Last Name is required"
		if len(postData['UserEmail']) == 0:
			errors['UserEmail'] = "Email is required"
		if not EMAIL_REGEX.match(postData['UserEmail']):
			errors['UserEmail'] = "Invalid email address"
		if len(userswithmatchingemail) >0:
			errors['UserEmail'] = "Unique email required"
		if len(postData['UserPW']) == 0:
			errors['UserPW'] = "Password is required"
		elif len(postData['UserPW']) < 8:
			errors['UserPW'] = "Password must be at least 8 characters long"
		if postData['UserPW'] != postData['UserCPW']:
			errors['cpwMatch'] = "Passwords Must Match!"
		return errors


	def loginValidator(self, postData):
		errors = {}
		userswithmatchingemail = User.objects.filter(email = postData['UserEmail'])
		if len(userswithmatchingemail) == 0:
			errors['emailnotfound'] = "This email is not yet registered"
		else:
			if userswithmatchingemail[0].password != postData['UserPW']:
				errors['incorrectpassword'] = "Password is incorrect"
		return errors

class TripManager(models.Manager):
	def createTripValidator(self, postData):
		errors = {}
		today = str(date.today())
		if len(postData['desc']) == 0:
			errors['desc'] = "Description is Required"
		elif len(postData['desc']) <5:
			errors['desc'] = "Meal name must be 5 characters"
		if len(postData['startDate']) == 0:
			errors['needsdate'] = "Start Date is required"
		elif postData['startDate'] < today:
			errors['toosoon'] = "Needs to be in the future"
		if len(postData['endDate']) == 0:
			errors['neededate'] = "End Date is required"
		if postData['endDate'] < today:
			errors['toosoon'] = "Needs to be in the future"
		if postData['endDate'] < postData['startDate']:
			errors['Please'] = "To date must be after From Date!"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
    description = models.TextField()
    creator = models.ForeignKey(User, related_name= 'trips_created', on_delete = models.CASCADE)
    favoritors = models.ManyToManyField(User, related_name='trips_favorited')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

# Create your models here.
