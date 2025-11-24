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
    
    @property
    def join_date(self):
        """Get join date from earliest internal experience"""
        earliest_exp = self.internal_experiences.order_by('from_date').first()
        return earliest_exp.from_date if earliest_exp else None
    
   
    
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

class EmployeePersonalDetails(models.Model):
    employee = models.OneToOneField(
        'Employee',
        on_delete=models.CASCADE,
        related_name='personal_details'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    contact_telephone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country_of_birth = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[
            ('Single', 'Single'),
            ('Married', 'Married'),
            ('Divorced', 'Divorced'),
            ('Widowed', 'Widowed'),
        ],
        blank=True,
        null=True
    )
    highest_education = models.CharField(
        max_length=100,
        choices=[
            ('High School', 'High School'),
            ('Diploma', 'Diploma'),
            ('Bachelor', "Bachelor's Degree"),
            ('Master', "Master's Degree"),
            ('Doctorate', 'Doctorate'),
        ],
        blank=True,
        null=True
    )
    working_rights = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="HR Admin Only - e.g., Citizen, Work Visa, etc."
    )
    
    # Medical Information
    allergies = models.TextField(
        blank=True,
        null=True,
        help_text="Any medical allergies"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Personal Details - {self.employee}"


class EmergencyContact(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    
    name = models.CharField(max_length=200)
    relationship = models.CharField(
        max_length=50,
        choices=[
            ('Parent', 'Parent'),
            ('Spouse', 'Spouse'),
            ('Child', 'Child'),
            ('Sibling', 'Sibling'),
            ('Friend', 'Friend'),
            ('Other', 'Other'),
        ]
    )
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.relationship})"
    
class PersonnelDocument(models.Model):
    DOCUMENT_TYPES = [
        ('Resume', 'Resume'),
        ('Application Form', 'Application Form'),
        ('Aptitude Test', 'Aptitude Test'),
        ('Interview Guide', 'Interview Guide'),
        ('Presentation', 'Presentation'),
        ('Training Checklist', 'Training Checklist'),
        ('Other', 'Other'),
    ]
    
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='personnel_documents'
    )
    upload_date = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file_name = models.CharField(max_length=255)
    document = models.FileField(upload_to='personnel_documents/%Y/%m/')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.file_name} ({self.upload_date})"
    

    
class Education(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='education_records'
    )
    institution = models.CharField(max_length=255)
    degree_course = models.CharField(max_length=255)
    department = models.CharField(max_length=200, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    certificate = models.FileField(
        upload_to='education_certificates/',
        null=True,
        blank=True,
        help_text="Upload certificate, transcript, or letter of completion"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-to_date', '-from_date']
    
    def __str__(self):
        return f"{self.degree_course} - {self.institution}"
    

class ExternalExperience(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='external_experiences'
    )  
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)    
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-from_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"
    

class Training(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='trainings'
    )
    training_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, blank=True, null=True)
    subject_matter = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Completed', 'Completed'),
            ('In Progress', 'In Progress'),
            ('Planned', 'Planned'),
        ],
        default='Completed'
    )
    certificate = models.FileField(
        upload_to='training_certificates/',
        null=True,
        blank=True,
        help_text="OPTIONAL: Upload certificate if available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-from_date']
    
    def __str__(self):
        return f"{self.training_name} ({self.from_date})"


class Certification(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    certification_name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    subject_matter = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    validity_period = models.DateField(
        null=True,
        blank=True,
        help_text="Expiry or validity end date"
    )
    does_not_expire = models.BooleanField(default=False)
    certificate = models.FileField(
        upload_to='certifications/',
        null=True,
        blank=True,
        help_text="OPTIONAL: Upload certificate if available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-from_date']
    
    def __str__(self):
        return f"{self.certification_name} - {self.issuing_organization}"
    
class Grading(models.Model):
    grade_code = models.CharField(max_length=10, unique=True)
    grade_name = models.CharField(max_length=100)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade_code']
    
    def __str__(self):
        return f"{self.grade_code} - {self.grade_name}"

class InternalExperience(models.Model):
    PRESENTATION_REASON_CHOICES = [
        ('Promotion', 'Promotion'),
        ('Transfer', 'Transfer'),
        ('Grading Review', 'Grading Review'),
    ]
    
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='internal_experiences')
    position_title = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    grading = models.ForeignKey('Grading', on_delete=models.SET_NULL, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    presentation_reason = models.CharField(max_length=50, choices=PRESENTATION_REASON_CHOICES, blank=True, null=True)
    presentation_document = models.FileField(upload_to='internal_experience_presentations/%Y/%m/', null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    results_document = models.FileField(upload_to='internal_experience_results/%Y/%m/', null=True, blank=True)
    final_comments = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-from_date']
    
    def __str__(self):
        current = " (Current)" if self.is_current else ""
        return f"{self.position_title} - {self.department}{current}"
