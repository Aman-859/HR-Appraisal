from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    division = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


   

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.role_name






class AppraisalCycle(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=100,blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("Draft", "Draft"),
            ("Active", "Active"),
            ("Closed", "Closed"),
        ],
        default="Draft",
    )

    def __str__(self):
        return f"{self.name} ({self.year})"
    

    
class AppraisalForm(models.Model):
    appraisal_cycle = models.ForeignKey("AppraisalCycle", on_delete=models.CASCADE)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="appraisals")
    supervisor = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True, related_name="supervised_appraisals")
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=[("Draft", "Draft"), ("Submitted", "Submitted"), ("Reviewed", "Reviewed"), ("Closed", "Closed")],
        default="Draft"
    )

    def __str__(self):
        return f"Appraisal - {self.employee} ({self.appraisal_cycle})"
    
class AppraisalKPIResponse(models.Model):
    appraisal_form = models.ForeignKey("AppraisalForm", on_delete=models.CASCADE, related_name="kpi_responses")
    kra = models.ForeignKey("KRA", on_delete=models.CASCADE)
    kpi = models.ForeignKey("KPI", on_delete=models.CASCADE)

    self_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    supervisor_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.appraisal_form.employee} - {self.kpi.name}"


class EmployeeObjective(models.Model):
    appraisal_form = models.ForeignKey("AppraisalForm", on_delete=models.CASCADE, related_name="objectives")
    objective = models.CharField(max_length=255)
    weightage = models.PositiveIntegerField()
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="objectives", null=True, blank=True)


    def __str__(self):
        return f"{self.objective} ({self.weightage}%)"


class EmployeeKPI(models.Model):
    objective = models.ForeignKey(EmployeeObjective, on_delete=models.CASCADE, related_name="kpis")
    name = models.CharField(max_length=255)
    target = models.CharField(max_length=255, blank=True, null=True)
    achieved = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="employee_profile"
)
    
    employee_id = models.CharField(max_length=20, unique=True)
    employee_salution = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    contact_number = models.IntegerField(default=0)

    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True)
    supervisor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
    
    @property
    def manager(self):
        """Return the supervisor of this employee's supervisor (if any)."""
        return self.supervisor.supervisor if self.supervisor else None
    
   
    
class KRA(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    kra_name = models.CharField(max_length=200)
    weightage = models.DecimalField(max_digits=5, decimal_places=2)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.kra_name} ({self.department})"

    def clean(self):
        # Get total weightage for department excluding this KRA (if updating)
        existing_total = KRA.objects.filter(department=self.department).exclude(pk=self.pk).aggregate(
            total=models.Sum("weightage")
        )["total"] or 0

        new_total = existing_total + (self.weightage or 0)

        if new_total > 100:
            raise ValidationError(
                f"Total KRA weightage for {self.department} would exceed 100% (currently {existing_total}%)."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # ensure clean() is called before save
        super().save(*args, **kwargs)

class KPI(models.Model):
    kra = models.ForeignKey("KRA", on_delete=models.CASCADE, related_name="kpis")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    weightage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.kra})"

    def clean(self):
        existing_total = KPI.objects.filter(kra=self.kra).exclude(pk=self.pk).aggregate(
            total=Sum("weightage")
        )["total"] or 0

        new_total = existing_total + (self.weightage or 0)

        if new_total > 100:
            raise ValidationError(
                f"Total KPI weightage for '{self.kra.kra_name}' cannot exceed 100%. "
                f"Currently at {existing_total}%."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)



class RatingMaster(models.Model):
    appraisal_cycle = models.CharField(max_length=100)   # text, not FK
    current_year = models.CharField(max_length=9)
    appraisal_id = models.IntegerField(blank=True,null=True)
    rating_score = models.IntegerField(blank=True,null=True)
    rating = models.CharField(max_length=100)

    create_date_time = models.DateTimeField(auto_now_add=True)
    update_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating_score} - {self.rating}"

class WeightageMaster(models.Model):
    appraisal_cycle = models.CharField(max_length=100)   # text, not FK
    current_year = models.CharField(max_length=9)
    appraisal_id = models.IntegerField(blank=True,null=True)

    weightage_employee = models.IntegerField()
    weightage_supervisor = models.IntegerField()
    weightage_manager1 = models.IntegerField()
    weightage_manager2 = models.IntegerField()

    create_date_time = models.DateTimeField(auto_now_add=True)
    update_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appraisal {self.appraisal_id} - {self.appraisal_cycle}"
    

class EmployeeKRA(models.Model):
    appraisal_form = models.ForeignKey("AppraisalForm", on_delete=models.CASCADE,null=True, blank=True)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    kra = models.ForeignKey("KRA", on_delete=models.CASCADE)
    approved_by_manager = models.BooleanField(default=False)

    class Meta:
        unique_together = ("employee", "kra","appraisal_form")

    def __str__(self):
        return f"{self.employee} - {self.kra} ({'Approved' if self.approved_by_manager else 'Not Approved'})"
