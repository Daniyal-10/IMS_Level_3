from api.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
# router.register(r'employee', EmployeeViewSet)
router.register(r'incident', IncidentTicketViewSet, basename='incident')
router.register(r'statusticket', StatusViewSet, basename='statusticket')
router.register(r'pocticket', POCViewSet, basename='pocticket')
router.register(r'incidenttype', IncidentTypeViewSet)
router.register(r'role', RoleViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'designation', DesignationViewSet)
router.register(r'factors', Contributing_factorsViewSet)
router.register(r'potential', PotentialSeverityView)
router.register(r'recurrency', RecurrencyViewSet)
router.register(r'risklevel', Risk_levelViewSet)
# router.register(r'riskassessment', RiskAssessmentView)
router.register(r'both', EmployeeUserViewSet)
router.register(r'status', StatusViewSet)

urlpatterns = [
    # path('role/', RoleView),
    # path('department/', DepartmentView),
    # path('designation/', DesignationView ),
    # path('customuser/', CustomUserView),
    # path('employee/', EmployeeView),
    # path('departmentpoc/', DepartmentPOCView),
    # path('incidenttype/', Incident_typeView),
    # path('contributingfactors/', Contributing_factorsView),
    # path('stakeholder/', stake_holderView),
    # path('incidentticket/', Incident_ticketView),
    # path('incidentticket2/', IncidentTicketDetails),
    # path('filterticket/<int:requestor_id>/', FilterTicket),
    # path('send-email/', send_test_email),
    # path('sent-otp/', email_otp),
    # path('verify-otp/', verify_otp),
    # path('request-reset/', request_reset_password),
    # path('verify-reset/', otp_verification),
    # path('reset-password/', reset_password),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('  ', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('resetpassword/', reset_passwordView),    # Just reset password
    # path('forgetpassword/', request_reset_password), #1  Forget password urls
    # path('otp_verify/', otp_verification),  #2
    # path('reset/', reset_password), #3
    # path("emp1/", employee_v),
    path('forgetpassword/', RequestPasswordReset.as_view() ),
    path('otpverify/', VerifyOtp.as_view() ),
    path('reset/', SetNewPassword.as_view() ),
    # path("emp2/", employee_v2),
    #********************ModelVIewSet****************
    # path('pocview/',Poc_view),
    path('',include(router.urls)),
]   