
from django.db import models
from django.contrib.auth.models import User

class TODO1(models.Model):
    status_choices=[
        ('C','COMPLETED'),
        ('P','PENDING')
    ]
    priority_choices=[
        ('1', '1'),
        ('2','2'),
        ('3','3'),
    
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2 , choices=status_choices)
    user = models.ForeignKey(User , on_delete=models.CASCADE) ##CASCADE means if user is deleted then his full "to do" should be deleted
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2 , choices=priority_choices)