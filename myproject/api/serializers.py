from .models import *
from rest_framework import serializers
from datetime import datetime
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class DesignationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Designation
        fields = "__all__"

class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Incident_type
        fields = "__all__"

class StakeHolderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stake_holder
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","first_name","last_name","email","password","role"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"        

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    class Meta: 
        model = Employee
        fields = "__all__"   

# Employee view with the user data also with the specific fields
class EmployeeProfile(serializers.ModelSerializer):
    Firstname = serializers.CharField(source = "user.first_name")
    Lastname = serializers.CharField(source = "user.last_name")
    Email = serializers.CharField(source = "user.email")
    Department = serializers.CharField(source = "designation_id.dep_id.name")

    class Meta:
        model = Employee
        fields = ['id','Firstname', 'Lastname','designation_id','Department','job_title','phone_no', 'Email']

class Department_pocSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Department_poc
        fields = "__all__"

class Incident_typeSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Incident_type
        fields = "__all__"

class Contributing_factorsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributing_factor
        fields = "__all__"

class Potential_severitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Potential_severity
        fields = "__all__"        

class RecurrencySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Recurrency
        fields = "__all__"  

class Risk_levelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk_level
        fields = "__all__"

# class RiskAssessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Risk_assessment
#         fields = "__all__"
class ImmediateAction_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Immediate_actions
        fields = "__all__"
        # exclude = ["incident_id"]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     id = data.pop('id')
    #     tokenid = data.pop('incident_id')
    #     data["action_taken_by"] = [
    #         i["user"]["full_name"] for i in EmployeeSerializer(instance.action_taken_by , many=True).data]
    #     return data



class contributing_factors_Serializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributing_factor
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
class IncidentStatusSerializer(serializers.ModelSerializer):
    # status = StatusSerializer()
    class Meta:
        model = Incident_status
        fields = "__all__"

# class riskassessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Risk_assessment
#         fields = "__all__"
# Creating Employee and user in this serializer 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","email","role","password"]
        extra_kwargs = {
        'password': {'write_only': True}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class EmployeeUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Employee
        fields = "__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)

        employee = Employee.objects.create(user=user, **validated_data)
        return employee
 
class Improvement_recommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Improvement_Recommendation
        fields = "__all__"

        # def to_representation(self, instance):
        #     data = super().to_representation(instance)
        #     data['incident_id'] = instance.incident.id
        #     data["action_description"] = instance.action_description
        #     # data["responsible_employee_id"] = 
        #     return data
        # fields = ["action_description","responsible_employee_id"]

class Follow_up_actionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow_up_action
        fields = "__all__"


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident_Evidence
        fields = ["file"]

#Example payload  
'''
{                                                                                       
  "requestor_id": 1,
  "report_type": 1,
  "location": "k",
"department":1,
  "description": "llllll",
  "contributing_factor": [3],                       
  "Individuals_involved": [4],
  "incident_witness": [3],
  "immediateActions": [
    {
      "employee_id": [1],
      "title": "nn",
      "description": "k"
    },
    {
      "employee_id": [2, 4],
      "title": "vm mjn",
      "description": "jjj"
    }
  ],
"incidentEvidences" : [],

}
'''
#MY payload        
'''
{
    "ImmediateAction": [
    {
      "employee_id": [1],
      "description": "k"
    }
    ],
    "contributing_factors": {
        "name": ""
    },
    "location": "",
    "requestor_id": null,
    "report_type": null,
    "department": null,
    "evidence": [],
    "ImmediateActions": [],
    "Individuals_invloved": [],
    "Witnesses": []
}
'''
#sample payload
'''
{
        "requestor_id": 1,
        "report_type": 1,
        "location": "bhopal status",
        "department": 1,
        "Immediateactions": [
            {
                "id": 12,
                "Description": "Fire was extinguished",
                "action_taken_by": [
                    3,
                    4
                ]
            },
            {
                "id": 13,
                "Description": "Aag bhujhana",
                "action_taken_by": [
                    4,
                    5
                ]
            }
        ],
        "Individuals_invloved": [
            2
        ],
        "Witnesses": [
            3,
            4
        ],
        "contributing_factors": [
            3,
            5
        ]
    }
'''
class Incident_ticketSerializer(serializers.ModelSerializer):
    Immediateactions = ImmediateAction_Serializer(many=True, required =False, allow_null=True)
    # follow_up = Follow_up_actionSerializer(many=True, required = False, allow_null=True)
    incident_evidences = EvidenceSerializer(many=True, required =False)
    status=StatusSerializer(many=True, read_only=True)


    class Meta:
        model = Incident_Ticket
        # fields = [
        #           'id',
        #           "requestor_id",
        #           "report_type",
        #           "location",
        #           "department",
        #           "incident_evidences",
        #           "assigned_POC",
        #           "Immediateactions",
        #           "Individuals_invloved",
        #           "Witnesses",
        #           "contributing_factors",
        #           "status",
        #           ]
        fields = '__all__'

    def create(self, validated_data):
        dep_id = validated_data["department"]
        
        #Poping to store there value cuz nested fields
        Individual_data = validated_data.pop("Individuals_invloved")
        incident_witness_data = validated_data.pop("Witnesses")
        factors_data = validated_data.pop("contributing_factors")
        Immediateactions = validated_data.pop("Immediateactions")
        incident_evidences = validated_data.pop("incident_evidences", [])
    
        # Assigning POC
        POC = dep_id.department_pocc.first()
        validated_data["assigned_POC"] = POC

        #ticket creation
        ticket = Incident_Ticket.objects.create(**validated_data)

        #status open
        open_status = Status.objects.get(id=1)
        status_data = {
            "status_id": open_status,
            "incident_id":ticket,
            "date_created":datetime.now(),
        }

        Incident_status.objects.create(**status_data)
        
        # Assigning Immediate Actions
        for action in Immediateactions:
            emp = action.pop("action_taken_by", [])
            action["incident_id"] = ticket
            IA = Immediate_actions.objects.create(**action)
            IA.action_taken_by.set(emp)
              
        # adding individuals involoved
        ticket.Individuals_invloved.set(Individual_data)
        # adding factors
        ticket.contributing_factors.set(factors_data)
        # adding witness
        ticket.Witnesses.set(incident_witness_data)

     # adding evidences
        for evidence in incident_evidences:
            Incident_Evidence.objects.create(incident_id = ticket, **evidence )

    # Customising ticket view
    def to_representation(self, instance): 

        rep =  super().to_representation(instance)   #in this we get the initial data from the model
        
        rep["Improvement_recommendations"] = [
            {
            "id": im.id,
            "action_description": im.action_description,
            "incident_id":im.incident_id.id,
            "responsible_employee_id": im.responsible_employee_id.user.id,
            "responsible_employee": im.responsible_employee_id.user.full_name()
        } for im in instance.Improvement_Recommendation.all()
        ]

        rep["Follow_up"] = [
            {
                "id": fw.id,
                "action_description":fw.action_description,
                "date_completed":fw.date_completed,
                "responsible_employee_id" : fw.responsible_employee_id.user.id,
                "responsible_employee" : fw.responsible_employee_id.user.full_name(),
                "incident_id":fw.incident_id.id
            } for fw in instance.follow_up.all()
        ]

        rep["status"] = [
                {
                # "id":s.id(),
                "name":s.status_id.name,
                "date_created": s.date_created
            } for s in instance.incident_status.all()
        ]

        rep["Immediateactions"] = [
            {
                "id": ia.id,
                "Description":ia.Description,
                "incident_id":ia.incident_id.id,
                "action_taken_by": [
                    {
                        "id": emp.id,
                        "user": emp.user.full_name()
                    } for emp in ia.action_taken_by.all()
                ]
            } for ia in instance.Immediateactions.all()
        ]
        

        rep["Potential_severity"] = instance.Potential_severity.name if instance.Potential_severity else None
        rep["recurrency"] = instance.recurrency.name if instance.recurrency else None
        rep["risk_level"] = instance.risk_level.name if instance.risk_level else None

        # rep["status"] = {
        #     "id":instance.status.id(),
        #     "name":instance.incident_status.name
        # }

        rep['Reportor'] = {
            "Name":instance.requestor_id.user.full_name(),
            "Designation": instance.requestor_id.designation_id.name,
        }

        rep['assigned_POC'] = instance.assigned_POC.employee_id.user.full_name() if instance.assigned_POC else None

        rep['report_type'] = instance.report_type.name if instance.report_type else None

        rep['contributing_factors'] = [factor.name for factor in instance.contributing_factors.all()]

        rep['department'] = {
            "id": instance.department.id,
            "name": instance.department.name    
        } if instance.department else None

        rep["Witnesses"] = [emp.user.full_name() for emp in instance.Witnesses.all()]

        rep["Individuals_invloved"] = [emp.user.full_name() for emp in instance.Individuals_invloved.all()]

        #popping unnecessary fields from the response
        rep.pop('requestor_id', None)
    
        return rep
        # ticket.refresh_from_db()
        # return ticket
    

# View for poc (Status) *********************************************************************************
class StatusViewSerializer(serializers.ModelSerializer):
    s=serializers.IntegerField(write_only=True)
    class Meta:
            model = Incident_Ticket
            fields = ["id","s"]

    def update(self, instance, validated_data):

        status_id = validated_data.pop('s')
        Incident_status.objects.create(
                    incident_id = instance,
                    status_id= Status.objects.get(pk=status_id),
                )
        return instance
    
# *************************************View for POC *********************************************************************************
class POCViewSerializer(serializers.ModelSerializer):
    Improvement_recommendations = Improvement_recommendationsSerializer(many =True, source='Improvement_Recommendation', read_only=True)
    Follow_up = Follow_up_actionSerializer(many=True, source= 'Follow_up_action', read_only=True)
    # Follow_up = Follow_up_actionSerializer(many =True)

    class Meta:
        model = Incident_Ticket
        fields = ["Improvement_recommendations","Follow_up","risk_level","recurrency","Potential_severity"]

    def update(self, instance, validated_data):
        improvement_data = self.context['request'].data.get('Improvement_recommendations', [])
        Follow_up = validated_data.pop("Follow_up",[])
        risk = validated_data.pop("risk_level")
        recurrency = validated_data.pop("recurrency")
        potential_severity = validated_data.pop("Potential_severity")

        if risk:
            instance.risk_level = risk
        if recurrency:
            instance.recurrency = recurrency
        if potential_severity:
            instance.Potential_severity = potential_severity

        # Improvemnt_recommendation
        for one in improvement_data:
            print(one)
            desc = one.get("action_description")
            emp = one.pop("responsible_employee_id", None)

            emp_instance = Employee.objects.get(id=emp)
            one["incident_id"] = instance
            Improvement_Recommendation.objects.create(
                incident_id = instance,
                responsible_employee_id = emp_instance,
                action_description = desc,
                )

        # follow up actions 
        for follow in Follow_up:
            desc = follow.get("action_description")
            emp_id = follow.get("responsible_employee_id")

            emp_instance = Employee.objects.get(id=emp_id)

            # follow["incident_id"] = instance
            Follow_up_action.objects.create(
                incident_id = instance,
                responsible_employee_id = emp_instance,
                action_description = desc,
                )
        instance.save() 
        
        return instance



#*******************Adding employee id in the ticket token ddataaaaaaaaaaaaa****************************
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #adding custom claims
        try:
            token['employee_id'] = user.employee.id
        except AttributeError:
            token['employee_id'] = None

        return token

# class IncidentTicketSerializer1(serializers.ModelSerializer):
#     Reporter = serializers.SerializerMethodField()
#     Department = DepartmentSerializer(source='department', read_only=True)
#     Report_Type = serializers.CharField(source='report_type.name', read_only=True)
#     Occurance_date = serializers.DateTimeField(source='occurence_date', read_only=True)
#     AssignedPOC = serializers.SerializerMethodField()
#     ContributingFactors = serializers.SerializerMethodField()

#     class Meta:
#         model = Incident_Ticket
#         fields = [
#             'id',
#             'Reporter',
#             'Report_Type',
#             'Department',
#             'Occurance_date',
#             'location',
#             'AssignedPOC',
#             'ContributingFactors'
#         ]

#     def get_Reporter(self, obj):
#         emp = obj.requestor_id
#         full_name = f"{emp.user.first_name} {emp.user.last_name}"
#         designation = emp.designation_id.name if emp.designation_id else ""
#         return {
#             "Name": full_name,
#             "Designation": designation
#         }

#     def get_AssignedPOC(self, obj):
#         if obj.assigned_POC and obj.assigned_POC.employee_id:
#             poc_user = obj.assigned_POC.employee_id.user
#             return {
#                 "Name": f"{poc_user.first_name} {poc_user.last_name}"
#             }
#         return None

#     def get_ContributingFactors(self, obj):
#         return [factor.name for factor in obj.contributing_factors.all()]

# class IncidentSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Incident_Ticket
#         # fields = "__all__"
#         fields = [
#             'id',
#             'requestor_id',
#             'report_type',
#             'department',
#             'occurence_date',
#             'location',
#             'assigned_POC',
#             'contributing_factors',
#         ]
    
    # def to_representation(self, instance):

    #     rep =  super().to_representation(instance)   #in this we get the initial data from the model

    #     rep['Reportor'] = {
    #         "Name":instance.requestor_id.user.full_name(),
    #         "Designation": instance.requestor_id.designation_id.name,
    #     }
    #     rep['assigned_POC'] = instance.assigned_POC.employee_id.user.full_name()
    #     rep['report_type'] = instance.report_type.name if instance.report_type else None

    #     rep['contributing_factors'] = [factor.name for factor in instance.contributing_factors.all()]

    #     rep['department'] = {
    #         "id": instance.department.id,
    #         "name": instance.department.name
    #     } if instance.department else None

    #     rep.pop('requestor_id', None)

    #     return rep
        









#******************************
# class IncidentTikcetSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Incident_Ticket
#         fields = "__all__"

# class IncidentTicketSerializer1(serializers.ModelSerializer):
#     Reporter = serializers.SerializerMethodField()
#     Department = DepartmentSerializer(source='department', read_only=True)
#     Report_Type = serializers.CharField(source='report_type.name', read_only=True)
#     Occurance_date = serializers.DateTimeField(source='occurence_date', read_only=True)
#     AssignedPOC = serializers.SerializerMethodField()
#     ContributingFactors = serializers.SerializerMethodField()

#     class Meta:
#         model = Incident_Ticket
#         fields = [
#             'id',
#             'Reporter',
#             'Report_Type',
#             'Department',
#             'Occurance_date',
#             'location',
#             'AssignedPOC',
#             'ContributingFactors'
#         ]

#     def get_Reporter(self, obj):
#         emp = obj.requestor_id
#         full_name = f"{emp.user.first_name} {emp.user.last_name}"
#         designation = emp.designation_id.name if emp.designation_id else ""
#         return {
#             "Name": full_name,
#             "Designation": designation
#         }

#     def get_AssignedPOC(self, obj):
#         if obj.assigned_POC and obj.assigned_POC.employee_id:
#             poc_user = obj.assigned_POC.employee_id.user
#             return {
#                 "Name": f"{poc_user.first_name} {poc_user.last_name}"
#             }
#         return None

#     def get_ContributingFactors(self, obj):
#         return [factor.name for factor in obj.contributing_factors.all()]
    

# class IncidentSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Incident_Ticket
#         # fields = "__all__"
#         fields = [
#             'id',
#             'requestor_id',
#             'report_type',
#             'department',
#             'occurence_date',
#             'location',
#             'assigned_POC',
#             'contributing_factors'
#         ]
#     def to_representation(self, instance):

#         rep =  super().to_representation(instance)   #in this we get the initial data from the model

#         rep['Reportor'] = {
#             "Name":instance.requestor_id.user.full_name(),
#             "Designation": instance.requestor_id.designation_id.name,
#         }
#         rep['assigned_POC'] = instance.assigned_POC.employee_id.user.full_name()
#         rep['report_type'] = instance.report_type.name if instance.report_type else None

#         rep['contributing_factors'] = [factor.name for factor in instance.contributing_factors.all()]

#         rep['department'] = {
#             "id": instance.department.id,
#             "name": instance.department.name
#         } if instance.department else None

#         rep.pop('requestor_id', None)

#         return rep
        