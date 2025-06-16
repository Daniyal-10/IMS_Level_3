from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Department_poc)
admin.site.register(Incident_type)
admin.site.register(Contributing_factor)
admin.site.register(Incident_Ticket)
admin.site.register(Incident_Evidence)
admin.site.register(Status)
admin.site.register(Incident_status)
admin.site.register(Potential_severity)
admin.site.register(Recurrency)
admin.site.register(Risk_level)
# admin.site.register(Risk_assessment)
admin.site.register(Improvement_Recommendation)
admin.site.register(Follow_up_action)
admin.site.register(Immediate_actions)
# admin.site.register(Immediate_action_employee)


