from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from meeting.forms import AddUserForm, SignUpForm
from .models import Profile
from django.contrib.auth.models import User
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Meeting
from django.core.mail import send_mail
from django.conf import settings
import requests
import json


def home(request):
    meetings = Meeting.objects.all()
	# Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		# Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'meetings':meetings})
    


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


def create_user(request):
	form = AddUserForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_user = form.save()
				messages.success(request, "User Created Successfuly")
				return redirect('home')
		return render(request, 'create_user.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
      


def users_page(request):
      users = User.objects.all()
      if request.user.is_authenticated:
        return render(request, 'users_page.html', {'users': users})
      else:
        return render(request, 'home.html')
      

def delete_user(request, pk):
	if request.user.is_authenticated:
		delete_it = User.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "User Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')



def update_user(request, pk):
	if request.user.is_authenticated:
		current_record = User.objects.get(id=pk)
		form = AddUserForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "User Has Been Updated!")
			return redirect('home')
		return render(request, 'update_user.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
      


def user_details_page(request, pk):
    if request.user.is_authenticated:
           # Look Up Records
        user = User.objects.get(id=pk)
        return render(request, 'user_details_page.html', {'user':user})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home') 
		
       


    

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def meeting_home(request):
    # Fetching all meetings
    all_meetings = Meeting.objects.all()

     # Calculate time remaining for each past meeting
    for meeting in all_meetings:
        time_difference = meeting.start_time - timezone.now()
        if time_difference.total_seconds() < 0:
            meeting.time_remaining = f"Overdue {time_difference.days} days ago"
        else:
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format time remaining as a string
            time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

            # Assign the formatted time remaining to the meeting object
            meeting.time_remaining = time_remaining_str
    
    # Check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'meeting_home.html', {'all_meetings': all_meetings})
    

def upcoming_meetings(request):
    # Filtering upcoming meetings
    upcoming_meetings = Meeting.objects.filter(start_time__gte=timezone.now()).order_by('start_time')

     # Calculate time remaining for each past meeting
    for meeting in upcoming_meetings:
        time_difference = meeting.start_time - timezone.now()
        if time_difference.total_seconds() < 0:
             meeting.time_remaining = f"Overdue {time_difference.days} days ago"
        else:
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format time remaining as a string
            time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

            # Assign the formatted time remaining to the meeting object
            meeting.time_remaining = time_remaining_str

    # Check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'upcoming.html', {'upcoming_meetings': upcoming_meetings,})
    


def past_meetings(request):
    # Fetching past meetings
    past_meetings = Meeting.objects.filter(start_time__lt=timezone.now()).order_by('-start_time')

    # Calculate time remaining for each past meeting
    for meeting in past_meetings:
        time_difference = meeting.start_time - timezone.now()

        if time_difference.total_seconds() < 0:
             meeting.time_remaining = f"Overdue {time_difference.days} days ago"
        else:
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format time remaining as a string
            time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

            # Assign the formatted time remaining to the meeting object
            meeting.time_remaining = time_remaining_str

    # Check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'past.html', {'past_meetings': past_meetings})

      
      
    


def schedule_meeting(request):
    if request.method == "POST":

        user = User.objects.all()

        title = request.POST.get('title')
        start_time_str = request.POST.get('start_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')  # Parse the string to datetime
        duration = request.POST.get('duration')
        organizer = request.POST.get('organizer')

        # Convert start_time to string in the required format
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')

        data = requests.post("https://api.zoom.us/v2/users/me/meetings", headers={
            'content-type': "application/json",
            "authorization": f"Bearer {request.session['zoom_access_token']}"
        }, data=json.dumps({
            "topic": title,
            "type": 2,
            "start_time": start_time_str,
        }))

        if data.status_code == 201:
            join_url = data.json().get("join_url")
            start_url = data.json().get("start_url")

            # Save meeting details to the database or perform any other necessary actions
            Meeting.objects.create(title=title, start_time=start_time, duration=duration, organizer=organizer, join_link=join_url)

            messages.success(request, 'Meeting created successfully.')

            # Send email to all registered users
            message = 'A meeting has been scheduled. Login to check status of the meeting.'
            for user in User.objects.all():
                send_mail(
                    'MSMS',  # TITLE
                    message,
                    'settings.EMAIL_HOST_USER',
                    [user.email],  # Send email to the user's email address
                    fail_silently=False
                )

            return redirect('meeting_home')
        else:
            return HttpResponse("Failed to create meeting. Please try again.")
    else:
        return render(request, 'create_meeting.html')
    

def meeting_details(request, pk):
    if request.user.is_authenticated:
           # Look Up Records
        meeting = Meeting.objects.get(id=pk)
        return render(request, 'meeting_details.html', {'meeting':meeting})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    

def delete_meeting(request, pk):
    if request.user.is_authenticated:
          delete_meeting = Meeting.objects.get(id=pk)
          delete_meeting.delete
          messages.success(request, "Meeting Deleted Successfully...")
          return redirect('meeting_home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')




def base64_encode(message):
    import base64
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def zoom_callback(request):
    code = request.GET["code"]
    data = requests.post(f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://127.0.0.1:8000/zoom/callback/", headers={
        "Authorization": "Basic " + base64_encode("dnpVj6NRb2dib4SeGacVA:HkMoq1itryW1pjdbc6dSyt8bRHWIf0RP")
    })
    print(data.text)
    request.session["zoom_access_token"] = data.json()["access_token"]

    return HttpResponse("Done")