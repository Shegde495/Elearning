from django.db import models
from django.contrib.auth.models import User

class course(models.Model):
    edited=models.ForeignKey(User,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=20)
    purchase_cost=models.DecimalField( max_digits=5, decimal_places=2,default=0.00)
    
    def __str__(self):
        return self.course_name
    
class description(models.Model):
    name = models.ForeignKey(course, on_delete=models.CASCADE)
    des=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.des
    
class purchase(models.Model):
    purchase_topic=models.ForeignKey(course, on_delete=models.CASCADE)
    purchased_by=models.CharField(max_length=20)
    
    def __str__(self):
        return self.purchased_by
    
class check(models.Model):
    check_topic=models.CharField(max_length=20)
    check_user=models.CharField(max_length=20)
    
    def __str__(self):
        return self.check_topic
   
    
class OTP(models.Model):
    otp=models.IntegerField( )
    
    