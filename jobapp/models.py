from django.db import models
from django.db.models import Q
from datetime import date
from django.contrib.auth.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.company_name
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} at {self.company}"
    


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    time = models.DateField(default=date.today)  
    Typework_choices = [
        ('A', 'B'),
        ('C', 'D'),
        ('E', 'F'),
        ('G', 'H'),
        ('I', 'J'),
    ]
    Typework = models.CharField(max_length=20, choices=Typework_choices)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    def __str__(self):
        return self.title
    


def search_jobs(query):
    return Job.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(company__company_name__icontains=query) | 
        Q(location__icontains=query) |
        Q(Typework__icontains=query)
    )

def search_jobsadmin(query):
    return Job.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(company__company_name__icontains=query) | 
        Q(location__icontains=query) |
        Q(Typework__icontains=query)
    )    


class custom(models.Model):
    custom_id = models.AutoField(primary_key=True)
    custom_name = models.CharField(max_length=255)
    custom_lastname = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position_applied = models.CharField(max_length=255, default='')
    date_applied = models.DateField(default=date.today)  
    status = models.CharField(max_length=100, default='')
    source = models.CharField(max_length=100, default='')
    tal_phon = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    cv_file = models.FileField(upload_to='cv_files/', default='', blank=True, null=True)  # กำหนด default ว่าง

    def __str__(self):
        return f"{self.custom_name}, {self.zip} at {self.company}"

    



















    # def search_jobs(query):
#     return Job.objects.filter(
#         Q(title__icontains=query) |  
#         Q(description__icontains=query) |  
#         Q(company__icontains=query) |  
#         Q(location__icontains=query) |   
#         Q(Typework__icontains=query)  
#         )

# def search_jobsadmin(query):
#     return Job.objects.filter(
#         Q(title__icontains=query) |  
#         Q(description__icontains=query) |  
#         Q(company__icontains=query) |  
#         Q(location__icontains=query) |   
#         Q(Typework__icontains=query)  
#         )