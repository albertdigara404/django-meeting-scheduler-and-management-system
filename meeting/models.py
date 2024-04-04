from django.db import models

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.IntegerField()  # Duration in minutes
    organizer = models.CharField(max_length=255)
    join_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
    

class MeetingIdea(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    idea = models.TextField()

    def __str__(self):
        return self.idea
    
    

class Profile(models.Model):
    user_id = models.IntegerField()



class AddUser(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")

