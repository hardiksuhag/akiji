from django.db import models

# Create your models here.
'''
note that all defaults are immaterial cuz we'll 
be setting every attribute indivisually anyway.
They are just there to avoid any errors during migration.
'''


class Name(models.Model):
    # question_text = models.CharField(max_length=100)
    # pub_date = models.DateTimeField('date published')
    name_text = models.CharField(max_length=100, default='defaultname')
    search_count = models.CharField(max_length=10, default="0")

    def __str__(self):
        return(self.name_text)


class User(models.Model):
    ans_given = models.CharField(max_length=100, default="-1")
    ans_real = models.CharField(max_length=100, default="-1")
    ip_address = models.CharField(max_length=100, default='defaultip')  # a complete string
    time_active = models.CharField(max_length=100, default='0')  # a number (maximum 86399)
    prob_list = models.TextField(default='')  # format- pk,probablity/pk,probablity (probablity is float)
    history = models.TextField(default='')  # format- pk,0/pk,1/pk,1

    def __str__(self):
        return(self.ip_address)


class Member(models.Model):
    member_name = models.CharField(max_length=100, default='defaultmem')  # name of member
    times_searched = models.CharField(max_length=100, default='0')  # a number

    def __str__(self):
        return(self.member_name)


class Question(models.Model):
    question_text = models.CharField(max_length=100, default='defaultques')  # the question text

    def __str__(self):
        return(self.question_text)


class Data(models.Model):
    times_yes = models.CharField(max_length=100, default='0')  # a number
    times_total = models.CharField(max_length=100, default='1')  # a number
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return(self.question.question_text+' for '+self.member.member_name)

class Search(models.Model):
    search_time = models.DateTimeField('time of search') # date time field..., probably 5.5 hrs before India
    name_searched = models.CharField(max_length=100, default="") # the person's name
    ip_address = models.CharField(max_length=100, default="IP dosen't exist") # the user's IP address
    is_correct = models.CharField(max_length=100, default="-1") # 0 or 1 depending on whether or not the answer given was correct

    def __str__(self):
        return(self.name_searched)
