from django.contrib import admin
from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "first_name", "last_name", "email", "role", "user", "status")
    search_fields = ("first_name", "last_name", "email", "employee_id")
    list_filter = ("role", "status", "department")

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(EmployeeObjective)
admin.site.register(EmployeeKRA)
admin.site.register(AppraisalForm)
admin.site.register(EmployeePersonalDetails)
admin.site.register(PersonnelDocument)
admin.site.register(EmergencyContact)
admin.site.register(Education)
admin.site.register(InternalExperience)
admin.site.register(Grading)


# Register your models here.
