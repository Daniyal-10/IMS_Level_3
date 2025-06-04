# from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate , login, logout
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache 
import random
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser


# @api_view(["GET", "POST", "PATCH", "DELETE"])
# def CustomUserView(request):
#     if request.method == "GET":
#         obj = CustomUser.objects.all()
#         serializer = CustomUserSerializer(obj, many=True)
#         return Response(serializer.data)
    

#     if request.method =="POST":              #IMP stepss [making single view for user and employee creation]
#         data = request.data
#         serializer_u = CustomUserSerializer(data = data)

#         #User creation to get the user id to pass in the employee
#         if serializer_u.is_valid():
#             role = Role.objects.get(id=data["role"])
        
#             user = CustomUser.objects.create(
#                 first_name=data["first_name"],
#                 last_name=data["last_name"],
#                 email=data["email"],
#                 role=role)
#             user.set_password(data["password"])
#             user.save()

#             # Now creating employee as saved user and got the user id
#             employee_data = {
#                 "designation_id": data["designation_id"],
#                 "job_title": data["job_title"],
#                 "phone_no": data["phone_no"],
#                 "user": user.id  # This will map to 'user_id'
#             }

#             serializer_e = EmployeeSerializer(data = employee_data)
#             if serializer_e.is_valid():
#                 serializer_e.save()
#                 response_data = {
#                         "user":CustomUserSerializer(user).data,
#                         "employee":serializer_e.data
#                 }
#                 return Response(response_data, status=status.HTTP_201_CREATED)
    
#             else:
#                 user.delete()
#                 return Response({"employee_errors": serializer_e.errors}, status=status.HTTP_400_BAD_REQUEST)
            
#         return Response({"user_errors": serializer_u.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == "PATCH":
#         data = request.data
#         obj = CustomUser.objects.get(id = data["id"])
#         serializer = CustomUserSerializer(obj, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors).render.acceptres
    
#     if request.method == "DELETE":
#         obj_id = request.data.get('id')
        
#         if not obj_id:
#             return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             CustomUser.objects.get(id=obj_id).delete()
#             return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
#         except CustomUser.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Creating User and Employee at the same time in this view but in the serializer
class EmployeeUserViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeUserSerializer

# Making some view using ModelViewSet

class RoleViewSet(viewsets.ModelViewSet):
    queryset =  Role.objects.all()
    serializer_class = RoleSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset =  Department.objects.all()
    serializer_class = DepartmentSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset =  Designation.objects.all()
    serializer_class = DesignationSerializer    

class IncidentTypeViewSet(viewsets.ModelViewSet):
    queryset =  Incident_type.objects.all()
    serializer_class = Incident_typeSerializer

class Contributing_factorsViewSet(viewsets.ModelViewSet):
    queryset =  Contributing_factor.objects.all()
    serializer_class = contributing_factors_Serializer    

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset =  Employee.objects.all()
#     serializer_class = EmployeeProfile

class DepartmentPOCViewSet(viewsets.ModelViewSet):
    queryset =  Department_poc.objects.all()
    serializer_class = Department_pocSerializer

class IncidentTypeViewSet(viewsets.ModelViewSet):
    queryset =  Incident_type.objects.all()
    serializer_class = Incident_typeSerializer

class ContributingFactorsViewSet(viewsets.ModelViewSet):
    queryset =  Contributing_factor.objects.all()
    serializer_class = Contributing_factorsSerializer

class StakeHolderViewSet(viewsets.ModelViewSet):
    queryset =  Stake_holder.objects.all()
    serializer_class = StakeHolderSerializer

    
class PotentialSeverityView(viewsets.ModelViewSet):
    queryset = Potential_severity.objects.all()
    serializer_class = Potential_severitySerializer

class RecurrencyViewSet(viewsets.ModelViewSet):
    queryset = Recurrency.objects.all()
    serializer_class = RecurrencySerializer

class Risk_levelViewSet(viewsets.ModelViewSet):
    queryset = Risk_level.objects.all()
    serializer_class = Risk_levelSerializer

class RiskAssessmentView(viewsets.ModelViewSet):
    queryset = Risk_assessment.objects.all()
    serializer_class = RiskAssessmentSerializer

class IncidentTicketViewSet(viewsets.ModelViewSet):
    queryset = Incident_Ticket.objects.all()
    serializer_class = Incident_ticketSerializer
    
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer