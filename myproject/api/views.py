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

# class RiskAssessmentView(viewsets.ModelViewSet):
#     queryset = Risk_assessment.objects.all()
#     serializer_class = RiskAssessmentSerializer



class POCViewSet(viewsets.ModelViewSet):
    queryset = Incident_Ticket.objects.all()
    serializer_class = POCViewSerializer
    
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Incident_Ticket.objects.all()
    serializer_class = StatusViewSerializer

class POCViewSet(viewsets.ModelViewSet):
    queryset = Incident_Ticket.objects.all()
    serializer_class = POCViewSerializer

@api_view(["PATCH"])
def Poc_view(request):
        if request.method == "PATCH":
            data = request.data
            obj = Incident_Ticket.objects.get(id = data["id"])
            serializer = Incident_ticketSerializer(obj, data=data, partial=True)

            if serializer.is_valid():
                IR =Improvement_Recommendation.objects.create(
                    incident_id =data["Improvement_recommendations"]["incident_id"],
                    action_description = data["Improvement_recommendations"]["action_description"],
                    responsible_employee_id = data["Improvement_recommendations"]["responsible_employee_id"],
                )
                IR.save()
                # serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)


#************************* Login/ Logout***************
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error":"Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid email or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")
    
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh":str(refresh),
            "access":str(refresh.access_token),
        })
    
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


#Permissions and Authentication for ticket
from rest_framework.permissions import BasePermission

class RoleBasedPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "employee" is request.method in ["POST","GET"]:
            return True
        if request.user.role == "assigned_POC" is request.method in ["POST","GET","PATCH"]:
            return True
        if request.user.role == "stake_holder" is request.method == "GET":
            return True
        return False    

# @permission_classes([RoleBasedPermissions,IsAuthenticated])
# @authentication_classes([JWTAuthentication])
class IncidentTicketViewSet(viewsets.ModelViewSet):
    queryset = Incident_Ticket.objects.all()
    serializer_class = Incident_ticketSerializer        
        

# Resst Password API
@api_view(["POST"])
def reset_passwordView(request):
    email = request.data.get("email")
    oldpassword = request.data.get("oldpassword")
    newpassword = request.data.get("newpassword")
    user = CustomUser.objects.get(email=email)
    if user.check_password(oldpassword):
        user.set_password(newpassword)
        user.save()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)



# #************************ Forget Password Api ************************************************
import random

otp_storage = {}
class RequestPasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist:
            return Response({"error":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = str(random.randint(100000,999999))

        otp_storage[email] = {
            'otp':otp,
            'verified':False
        }

        print(f"Otp for {email}:{otp}")

        send_mail(
        subject="Password reset OTP",
        message=f"Your OTP for Password reset is: {otp}.",
        from_email= "workwithdaniyall@gmail.com",
        recipient_list=[email],
        fail_silently=False
        )

        return Response({"message":"Otp send to your email."}, status=status.HTTP_200_OK)


class VerifyOtp(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error":"Email and otp are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if email not in otp_storage:
            return Response({"error":"otp expired or not requested"}, status=status.HTTP_400_BAD_REQUEST)
        
        stored_otp_data = otp_storage[email]

        #verifying the otp 
        if stored_otp_data['otp'] == otp:
            otp_storage[email]["verified"] = True
            return Response({"message":"Otp verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Invalied Otp"})
        

class SetNewPassword(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password") 

        if not email or not new_password:
            return Response({"error":"Email and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP was verified
        if email not in otp_storage or not otp_storage[email].get('verified'):
            return Response(
                {"error": "OTP not verified - please complete OTP verification first"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save() 
            
        # Clear the OTP after successful password change
            if email in otp_storage:
                del otp_storage[email]

            return Response({"message":"Password changed successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


    
    
        

