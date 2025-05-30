from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# superuser dan@gmail.com   1234

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)



class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    username = None           # removing user field
    email = models.EmailField(_("email address"), unique=True)  #setting it as username 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return f"{self.first_name}{self.last_name}"

    def __str__(self):
        return self.email    
    
class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class Designation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    dep_id = models.ForeignKey(Department,on_delete=models.CASCADE)    

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee")
    id = models.AutoField(primary_key=True)
    designation_id = models.ForeignKey(Designation, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
   

class Department_poc(models.Model):
    id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="department_pocc")
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Stake_holder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Incident_type(models.Model):
    id = models.AutoField(primary_key=True)
    name  =models.CharField(max_length=40)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

class Contributing_factor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


#New addons
class Incident_Evidence(models.Model):
    id = models.AutoField(primary_key=True)
    incident_id = models.ForeignKey('Incident_Ticket', on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence')

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Incident_status(models.Model):
    id = models.AutoField(primary_key=True)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    incident_id = models.ForeignKey('Incident_Ticket', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

class Potential_severity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
class Recurrency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
class Risk_level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Risk_assessment(models.Model):
    id = models.AutoField(primary_key=True)
    severity = models.ForeignKey(Potential_severity,on_delete=models.CASCADE)
    recurrency = models.ForeignKey(Recurrency, on_delete=models.CASCADE)
    risk_level = models.ForeignKey(Risk_level, on_delete=models.CASCADE)

class Improvement_Recommendation(models.Model):
    id = models.AutoField(primary_key=True)
    action_description = models.CharField(max_length=500)
    responsible_employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    incident_id = models.ForeignKey('Incident_Ticket', on_delete=models.CASCADE)

class Follow_up_action(models.Model):
    id = models.AutoField(primary_key=True)
    action_description = models.CharField(max_length=500)
    date_completed = models.DateTimeField()
    responsible_employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    incident_id = models.ForeignKey('Incident_Ticket', on_delete=models.CASCADE)


class Immediate_actions(models.Model):
    id = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=500)
    incident_id = models.ForeignKey('Incident_Ticket', on_delete=models.CASCADE, null=True)
    action_taken_by = models.ManyToManyField(Employee, db_table='Immediate_action_employee',related_name='action_employee')
    

# class Immediate_action_employee(models.Model):
#     id = models.AutoField(primary_key=True)
#     immediate_action_id = models.ForeignKey('Immediate_actions', on_delete=models.CASCADE)
#     employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    


#Final Ticket
class Incident_Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    requestor_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_type = models.ForeignKey(Incident_type, on_delete=models.CASCADE)
    occurence_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100)
    assigned_POC = models.ForeignKey(Department_poc, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    evidence = models.ForeignKey(Incident_Evidence, on_delete=models.CASCADE, null=True)
    contributing_factors = models.ManyToManyField(Contributing_factor , db_table="Incident_factor")
    # # New fields
    Individuals_invloved = models.ManyToManyField(Employee, db_table="Individuals_involved", related_name='individuals_involved')
    Witnesses = models.ManyToManyField(Employee, db_table="Incident_witness", related_name='witness') 
    ImmediateActions = models.ForeignKey(Immediate_actions,on_delete=models.CASCADE, null=True, related_name='action_taken')
    Risk_assessment = models.ForeignKey(Risk_assessment, on_delete=models.CASCADE, null=True)
    Improvement_recommendations = models.ManyToManyField(Employee, through="Improvement_Recommendation", related_name='Improvements')
    Follow_up = models.ManyToManyField(Employee,through="Follow_up_action", related_name='follow_up_tickets')
    status = models.ManyToManyField(Status, through = "Incident_status", related_name='ticket_status')


