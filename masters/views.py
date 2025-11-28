from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Department
from .forms import DepartmentForm
from .forms import EmployeeObjectiveForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Role
from .forms import RoleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AppraisalCycle , Employee , KRA , KPI 
from .forms import AppraisalCycleForm, EmployeeForm , KRAForm , KPIForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import RatingMaster, WeightageMaster
from .forms import RatingMasterForm, WeightageMasterForm ,EmployeeKPIFormSet
from .models import Department, Country, State, City , PersonnelDocument ,EmergencyContact , EmployeePersonalDetails ,Education
from .forms import DepartmentForm
from .models import Employee, KRA, KPI ,ExternalExperience ,Certification ,Training
from .models import AppraisalCycle, Employee  , InternalExperience , Grading
from .models import AppraisalCycle, AppraisalForm, Employee, KRA
from .models import EmployeeObjective
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from dateutil.relativedelta import relativedelta
from datetime import date
# List view
@login_required
def list_departments(request):
    departments = Department.objects.all()
    for session in Session.objects.all():
        data = session.get_decoded()
        print("Session Key:", session.session_key)
        print("Decoded data:", data)

        uid = data.get('_auth_user_id')
        if uid:
            user = User.objects.get(pk=uid)
            print("Logged in as:",user.username)
    return render(request, "masters/departments_list.html", {"departments": departments})

# Add view
@login_required


def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        division = request.POST.get("division")
        country_name = request.POST.get("country")
        state_name = request.POST.get("state")
        city_name = request.POST.get("city")

        # Prevent saving if values missing
        if not (country_name and state_name and city_name):
            return render(request, "masters/add_department.html", {
                "form": DepartmentForm(),
                "error": "Please select country, state and city."
            })

        country, _ = Country.objects.get_or_create(name=country_name)
        state, _ = State.objects.get_or_create(name=state_name, country=country)
        city, _ = City.objects.get_or_create(name=city_name, state=state)

        Department.objects.create(
            name=name,
            division=division,
            country=country,
            state=state,
            city=city
        )
        return redirect("masters:list_departments")

    return render(request, "masters/departments_form.html", {"form": DepartmentForm()})


# Edit view
@login_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("masters:list_departments")
    else:
        form = DepartmentForm(instance=department)
    return render(request, "masters/departments_form.html", {"form": form, "title": "Edit Department"})

# Delete view
@login_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        return redirect("masters:list_departments")
    return render(request, "masters/departments_confirm_delete.html", {"department": department})

class RoleList(LoginRequiredMixin, ListView):
    model = Role
    template_name = "masters/roles_list.html"
    context_object_name = "roles"
    login_url = '/accounts/login/'      # where to redirect if not logged in
    redirect_field_name = 'next'

class RoleCreate(LoginRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = "masters/roles_form.html"
    success_url = reverse_lazy("masters:roles_list")
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class RoleUpdate(LoginRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = "masters/roles_form.html"
    success_url = reverse_lazy("masters:roles_list")
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class RoleDelete(LoginRequiredMixin, DeleteView):
    model = Role
    template_name = "masters/roles_confirm_delete.html"
    success_url = reverse_lazy("masters:roles_list")
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

class AppraisalCycleList(LoginRequiredMixin, ListView):
    model = AppraisalCycle
    template_name = "masters/cycles_list.html"
    context_object_name = "cycles"
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class AppraisalCycleCreate(LoginRequiredMixin, CreateView):
    model = AppraisalCycle
    form_class = AppraisalCycleForm
    template_name = "masters/cycles_form.html"
    success_url = reverse_lazy("masters:cycles_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class AppraisalCycleUpdate(LoginRequiredMixin, UpdateView):
    model = AppraisalCycle
    form_class = AppraisalCycleForm
    template_name = "masters/cycles_form.html"
    success_url = reverse_lazy("masters:cycles_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class AppraisalCycleDelete(LoginRequiredMixin, DeleteView):
    model = AppraisalCycle
    template_name = "masters/cycles_confirm_delete.html"
    success_url = reverse_lazy("masters:cycles_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "masters/employees_list.html"
    context_object_name = "employees"
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "masters/employees_form.html"
    success_url = reverse_lazy("masters:employees_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "masters/employees_form.html"
    success_url = reverse_lazy("masters:employees_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = "masters/employees_confirm_delete.html"
    success_url = reverse_lazy("masters:employees_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"

class KRAList(LoginRequiredMixin, ListView):
    model = KRA
    template_name = "masters/kras_list.html"
    context_object_name = "kras"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        return (
            KRA.objects
            .select_related("department")
            .order_by("department__name", "kra_name")
        )


class KRACreate(LoginRequiredMixin, CreateView):
    model = KRA
    form_class = KRAForm
    template_name = "masters/kras_form.html"
    success_url = reverse_lazy("masters:kras_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class KRAUpdate(LoginRequiredMixin, UpdateView):
    model = KRA
    form_class = KRAForm
    template_name = "masters/kras_form.html"
    success_url = reverse_lazy("masters:kras_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class KRADelete(LoginRequiredMixin, DeleteView):
    model = KRA
    template_name = "masters/kras_confirm_delete.html"
    success_url = reverse_lazy("masters:kras_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"

class KPIList(LoginRequiredMixin, ListView):
    model = KPI
    template_name = "masters/kpis_list.html"
    context_object_name = "kpis"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        return KPI.objects.select_related("kra", "kra__department").order_by("kra__department__name", "kra__kra_name", "name")


class KPICreate(LoginRequiredMixin, CreateView):
    model = KPI
    form_class = KPIForm
    template_name = "masters/kpis_form.html"
    success_url = reverse_lazy("masters:kpis_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class KPIUpdate(LoginRequiredMixin, UpdateView):
    model = KPI
    form_class = KPIForm
    template_name = "masters/kpis_form.html"
    success_url = reverse_lazy("masters:kpis_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"


class KPIDelete(LoginRequiredMixin, DeleteView):
    model = KPI
    template_name = "masters/kpis_confirm_delete.html"
    success_url = reverse_lazy("masters:kpis_list")
    login_url = "/accounts/login/"
    redirect_field_name = "next"








def rating_list(request):
    ratings = RatingMaster.objects.all()
    return render(request, "masters/rating_list.html", {"ratings": ratings})

def rating_create(request):
    if request.method == "POST":
        form = RatingMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("masters:rating_list")
    else:
        form = RatingMasterForm()
    return render(request, "masters/rating_form.html", {"form": form})

def rating_update(request, pk):
    rating = get_object_or_404(RatingMaster, pk=pk)
    if request.method == "POST":
        form = RatingMasterForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect("masters:rating_list")
    else:
        form = RatingMasterForm(instance=rating)
    return render(request, "masters/rating_form.html", {"form": form})

def rating_delete(request, pk):
    rating = get_object_or_404(RatingMaster, pk=pk)
    if request.method == "POST":
        rating.delete()
        return redirect("masters:rating_list")
    return render(request, "masters/rating_confirm_delete.html", {"rating": rating})


def weightage_list(request):
    weightages = WeightageMaster.objects.all()
    return render(request, "masters/weightage_list.html", {"weightages": weightages})

def weightage_create(request):
    if request.method == "POST":
        form = WeightageMasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("masters:weightage_list")
    else:
        form = WeightageMasterForm()
    return render(request, "masters/weightage_form.html", {"form": form})

def weightage_update(request, pk):
    weightage = get_object_or_404(WeightageMaster, pk=pk)
    if request.method == "POST":
        form = WeightageMasterForm(request.POST, instance=weightage)
        if form.is_valid():
            form.save()
            return redirect("masters:weightage_list")
    else:
        form = WeightageMasterForm(instance=weightage)
    return render(request, "masters/weightage_form.html", {"form": form})

def weightage_delete(request, pk):
    weightage = get_object_or_404(WeightageMaster, pk=pk)
    if request.method == "POST":
        weightage.delete()
        return redirect("masters:weightage_list")
    return render(request, "masters/weightage_confirm_delete.html", {"weightage": weightage})




from .models import EmployeeKRA
@login_required


@login_required
def appraisal_form_view(request, appraisal_id):
    appraisal_form = get_object_or_404(AppraisalForm, pk=appraisal_id)

    
    employee = appraisal_form.employee

  
    viewer = get_object_or_404(Employee, user=request.user)

    is_manager = viewer.role.role_name.lower() == "manager"

    if is_manager:
       
        kras = KRA.objects.filter(
            department=employee.department
        ).prefetch_related("kpis")
    else:
       
        visible_kra_ids = EmployeeKRA.objects.filter(
            employee=employee,
            appraisal_form=appraisal_form
        ).values_list("kra_id", flat=True)

        kras = KRA.objects.filter(
            department=employee.department,
            id__in=visible_kra_ids
        ).prefetch_related("kpis")

    objectives = EmployeeObjective.objects.filter(
        appraisal_form=appraisal_form,
        employee=employee
    )

    
    if request.method == "POST" and is_manager:
        checked_kra_ids = {
            int(kra_id.split("_")[-1])
            for kra_id in request.POST.keys()
            if kra_id.startswith("kra_visible_")
        }

       
        EmployeeKRA.objects.filter(
            employee=employee,
            appraisal_form=appraisal_form
        ).exclude(kra_id__in=checked_kra_ids).delete()

        
        existing_kra_ids = set(EmployeeKRA.objects.filter(
            employee=employee,
            appraisal_form=appraisal_form
        ).values_list("kra_id", flat=True))

        new_kra_ids = checked_kra_ids - existing_kra_ids
        EmployeeKRA.objects.bulk_create([
            EmployeeKRA(employee=employee, appraisal_form=appraisal_form, kra_id=kra_id)
            for kra_id in new_kra_ids
        ])

        messages.success(request, "KRA visibility updated.")
        return redirect("masters:appraisal_form", appraisal_id=appraisal_form.id)

    context = {
        "employee": employee,   
        "viewer": viewer,       
        "appraisal": appraisal_form,
        "kras": kras,
        "objectives": objectives,
        "is_manager": is_manager,
    }
    return render(request, "appraisal/form.html", context)






def team_appraisal_list(request):
    employee = get_object_or_404(Employee, user=request.user)
    active_cycle = AppraisalCycle.objects.filter(status="Active").first()

    forms = AppraisalForm.objects.none()  

    if active_cycle:
        role_name = employee.role.role_name.lower()

        if role_name == "manager":
            
            forms = AppraisalForm.objects.filter(
                employee__department=employee.department,
                appraisal_cycle=active_cycle
            ).exclude(employee=employee)

        elif role_name in ["supervisor", "supervisior"]:  
            
            forms = AppraisalForm.objects.filter(
                employee__supervisor=employee,
                appraisal_cycle=active_cycle
            )

    context = {"team_appraisal_forms": forms}
    return render(request, "masters/team_appraisal_list.html", context)






# def add_objective(request, appraisal_id):
#     appraisal = get_object_or_404(AppraisalForm, pk=appraisal_id)

#     if request.method == "POST":
#         form = EmployeeObjectiveForm(request.POST)
#         if form.is_valid():
#             objective = form.save(commit=False)
#             objective.appraisal_form = appraisal
#             objective.save()
#             return redirect("masters:appraisal_form", appraisal_id=appraisal.id)
#     else:
#         form = EmployeeObjectiveForm()

#     return render(request, "appraisal/add_objective.html", {
#         "form": form,
#         "appraisal": appraisal
#     })

def add_objective(request, appraisal_id):
    appraisal_form = get_object_or_404(AppraisalForm, pk=appraisal_id)

    if request.method == "POST":
        form = EmployeeObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.appraisal_form = appraisal_form

            # ✅ fetch Employee linked to logged-in user
            employee = get_object_or_404(Employee, user=request.user)
            objective.employee = employee
            objective.save()

            kpi_formset = EmployeeKPIFormSet(request.POST, instance=objective)
            if kpi_formset.is_valid():
                kpi_formset.save()

            return redirect("masters:appraisal_form", appraisal_id=appraisal_id)
    else:
        form = EmployeeObjectiveForm()
        kpi_formset = EmployeeKPIFormSet()

    return render(
        request,
        "appraisal/add_objective.html",
        {
            "form": form,
            "appraisal": appraisal_form,
            "kpi_formset": kpi_formset,
        },
    )




def my_appraisal_redirect(request):
    employee = get_object_or_404(Employee, user=request.user)
    active_cycle = AppraisalCycle.objects.filter(status="Active").first()

    if active_cycle:
        appraisal_form = AppraisalForm.objects.filter(
            employee=employee, appraisal_cycle=active_cycle
        ).first()

        if appraisal_form:
            return redirect("masters:appraisal_form", appraisal_id=appraisal_form.id)
        else:
            messages.error(request, "No appraisal form found for you in the active cycle.")
            return redirect("masters:cycles_list")
    else:
        messages.error(request, "No active appraisal cycle.")
        return redirect("masters:cycles_list")


@login_required
def review_list_form(request):
    employee = get_object_or_404(Employee,user = request.user)
    draft_forms = AppraisalForm.objects.filter(status="Draft")

    context={
        "draft_forms":draft_forms,
        "employee":employee
    }
    return render(request,"appraisal/review_list.html",context)


def is_hr_admin(user):
    """
    Check if user is HR Admin
    Based on Role model - assuming HR Admin role exists
    """
    try:
        employee = Employee.objects.get(user=user)
        # Check if employee's role is HR Admin
        return employee.role and employee.role.role_name.lower() in ['hr admin', 'hr', 'admin']
    except Employee.DoesNotExist:
        return False
    
 
def calculate_months_from_experiences(experiences):
    """
    Helper function to calculate total months from any experience list
    Returns: integer (total months)
    """
    total_months = 0
    
    for exp in experiences:
        # Get end date (today if still working)
        end_date = exp.to_date if exp.to_date else date.today()
        
        # Skip if dates are invalid (end before start)
        if exp.to_date and exp.to_date < exp.from_date:
            continue
        
        # Calculate months
        delta = relativedelta(end_date, exp.from_date)
        months = (delta.years * 12) + delta.months
        
        # Only add positive months
        if months > 0:
            total_months += months
    
    return total_months

def format_experience(total_months):
    """
    Convert months to readable format
    Returns: "5 years, 3 months" or "N/A"
    """
    if total_months == 0:
        return "N/A"
    
    years = total_months // 12
    months = total_months % 12
    
    if years > 0 and months > 0:
        return f"{years} years, {months} months"
    elif years > 0:
        return f"{years} years"
    else:
        return f"{months} months"

def calculate_internal_experience(employee):
    """
    Calculate Synnex experience (Internal only)
    Returns: "5 years, 3 months" or "N/A"
    """
    internal_experiences = InternalExperience.objects.filter(employee=employee)
    if not internal_experiences.exists():
        return "N/A"
    
    total_months = calculate_months_from_experiences(internal_experiences)
    return format_experience(total_months)

def calculate_external_experience(employee):
    """
    Calculate External experience (Other companies)
    Returns: "3 years, 6 months" or "N/A"
    """
    external_experiences = ExternalExperience.objects.filter(employee=employee) 
    if not external_experiences.exists():
        return "N/A"
    
    total_months = calculate_months_from_experiences(external_experiences)
    return format_experience(total_months)

def calculate_total_experience(employee):
    """
    Calculate Total experience (External + Internal)
    REUSES the other functions!
    Returns: "10 years, 6 months" or "N/A"
    """
    external_experiences = ExternalExperience.objects.filter(employee=employee)
    internal_experiences = InternalExperience.objects.filter(employee=employee)
    
    if not external_experiences.exists() and not internal_experiences.exists():
        return "N/A"
    
    external_months = calculate_months_from_experiences(external_experiences)
    internal_months = calculate_months_from_experiences(internal_experiences)
    total_months = external_months + internal_months
    return format_experience(total_months)

@login_required
def emp_profile(request, employee_id=None):
    current_is_hr = is_hr_admin(request.user)
    if employee_id and current_is_hr:
        employee = get_object_or_404(Employee, employee_id=employee_id)
    else:
        employee = get_object_or_404(Employee, user=request.user)
    
    personal, _ = EmployeePersonalDetails.objects.get_or_create(employee=employee)
    emergency_contacts = EmergencyContact.objects.filter(employee=employee).first()
    internal_experience = InternalExperience.objects.filter(employee=employee)
    
     
    current_internal = internal_experience.filter(is_current=True).first()
    current_grading = current_internal.grading if current_internal else None

    synnex_experience = calculate_internal_experience(employee)
    total_experience = calculate_total_experience(employee)

    documents = employee.personnel_documents.all()
    education = employee.education_records.all()
    external_experience = employee.external_experiences.all()
    certifications = employee.certifications.all()
    trainings = employee.trainings.all()
    
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == 'upload_document':
            try:
                PersonnelDocument.objects.create(
                    employee=employee,
                    document_type=request.POST.get("document_type"),
                    file_name=request.POST.get("file_name"),
                    document=request.FILES.get("document"),
                    notes=request.POST.get("notes", "")
                )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')
        
        elif form_type == 'delete_document':
            try:
                document_id = request.POST.get("doc_id")
                doc = PersonnelDocument.objects.get(id=document_id, employee=employee)
                doc.delete()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')
        
        elif form_type == "update_employee":
            try:
                if current_is_hr:
                    employee.first_name = request.POST.get("first_name")
                    employee.last_name = request.POST.get("surname")
                    employee.contact_number = request.POST.get("contact_number")
                    employee.email = request.POST.get("email")
                    employee.join_date = request.POST.get('service_start_date')
                    employee.save()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "update_personal":
            try:
                personal.date_of_birth = request.POST.get("dob")
                personal.gender = request.POST.get("gender")
                personal.contact_telephone = request.POST.get("phone")
                personal.address = request.POST.get("address")
                personal.country_of_birth = request.POST.get("country_of_birth")
                personal.marital_status = request.POST.get("marital_status")
                personal.highest_education = request.POST.get("highest_education")
                personal.nationality = request.POST.get("nationality")
                personal.allergies = request.POST.get("allergies")

                if current_is_hr:
                    personal.working_rights = request.POST.get("working_rights")

                personal.save()

                ec_name = request.POST.get("ec_name")
                if ec_name:
                    if emergency_contacts:
                        emergency_contacts.name = ec_name
                        emergency_contacts.relationship = request.POST.get("ec_relationship")
                        emergency_contacts.contact_number = request.POST.get("ec_phone")
                        emergency_contacts.save()
                    else:
                        EmergencyContact.objects.create(
                            employee=employee,
                            name=ec_name,
                            relationship=request.POST.get("ec_relationship"),
                            contact_number=request.POST.get("ec_phone")
                        )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "add_education":
            try:
                Education.objects.create(
                    employee=employee,
                    institution=request.POST.get("institution"),
                    degree_course=request.POST.get("degree"),
                    from_date=request.POST.get("start_date"),
                    to_date=request.POST.get("end_date") or None,
                    certificate=request.FILES.get("certificate"),
                    department = request.POST.get('department'),
                    grade = request.POST.get('grade')
                )
            except Exception as e:
                print(f"Error: {e}")
            if employee_id:
                return redirect(f'/masters/employee-profile/{employee.employee_id}/?section=education&accordion=edu')
            else:
                return redirect('/masters/employee-profile/?section=education&accordion=edu')
        
        elif form_type == "delete_education":
            try:
                education_id = request.POST.get("education_id")
                edu = Education.objects.get(id=education_id, employee=employee)
                edu.delete()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "add_external_experience":
            try:
                ExternalExperience.objects.create(
                    employee=employee,
                    company=request.POST.get("company"),
                    job_title=request.POST.get("job_title"),
                    department=request.POST.get("department"),
                    from_date=request.POST.get("start_date"),
                    to_date=request.POST.get("end_date") or None,
                    is_current=not request.POST.get("end_date"),
                    responsibilities=request.POST.get("responsibilities", "")
                )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')
        
        elif form_type == "delete_external_experience":
            try:
                experience_id = request.POST.get("experience_id")
                exp = ExternalExperience.objects.get(id=experience_id, employee=employee)
                exp.delete()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "add_training":
            try:
                Training.objects.create(
                    employee=employee,
                    training_name=request.POST.get("training_name"),
                    provider=request.POST.get("provider"),
                    subject_matter=request.POST.get("subject_matter"),
                    from_date=request.POST.get("start_date"),
                    to_date=request.POST.get("end_date") or None,
                    status=request.POST.get("status", "Completed"),
                    certificate=request.FILES.get("certificate")
                )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "delete_training":
            try:
                training_id = request.POST.get("training_id")
                training = Training.objects.get(id=training_id, employee=employee)
                training.delete()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "add_certification":
            try:
                expiry_date = request.POST.get("expiry_date") or None
                Certification.objects.create(
                    employee=employee,
                    certification_name=request.POST.get("certificate_name"),
                    issuing_organization=request.POST.get("issuing_org"),
                    subject_matter=request.POST.get("subject_matter"),
                    from_date=request.POST.get("issue_date"),
                    validity_period=expiry_date,
                    does_not_expire=not expiry_date,
                    certificate=request.FILES.get("certificate_file")
                )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == "delete_certification":
            try:
                certification_id = request.POST.get("certification_id")
                cert = Certification.objects.get(id=certification_id, employee=employee)
                cert.delete()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')

        elif form_type == 'add_internal_experience':
            try:
                position_title = request.POST.get('position_title')
                department_id = request.POST.get('department')
                grading_id = request.POST.get('grading')
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date') or None
                is_current = request.POST.get('is_current') == 'true'
                presentation_reason = request.POST.get('presentation_reason', '')
                comments = request.POST.get('comments', '')
                final_comments = request.POST.get('final_comments', '')
                responsibilities = request.POST.get('responsibilities', '')
                
                presentation_doc = request.FILES.get('presentation_doc')
                results_doc = request.FILES.get('results_doc')

                if is_current:
                    InternalExperience.objects.filter(
                        employee=employee,
                        is_current=True
                    ).update(is_current=False, to_date=from_date)
                
                department = Department.objects.get(pk=department_id) if department_id else None
                grading = Grading.objects.get(pk=grading_id) if grading_id else None

                InternalExperience.objects.create(
                    employee=employee,
                    position_title=position_title,
                    department=department,
                    grading=grading,
                    from_date=from_date,
                    to_date=to_date,
                    is_current=is_current,
                    presentation_reason=presentation_reason,
                    comments=comments,
                    final_comments=final_comments,
                    responsibilities=responsibilities,
                    presentation_document=presentation_doc,
                    results_document=results_doc
                )
            except Exception as e:
                print(f"Error: {e}")
            return redirect('masters:emp_profile_view', employee_id=employee.employee_id) if employee_id else redirect('masters:emp_profile')
            
    context = {
        'employee': employee,
        'personal': personal,
        'emergency_contacts': emergency_contacts,
        'documents': documents,
        'education': education,
        'external_experience': external_experience,
        'certifications': certifications,
        'trainings': trainings,
        'internal_experience': internal_experience,
        'current_grading': current_grading,   
        'departments': Department.objects.all(),
        'gradings': Grading.objects.all().order_by('grade_code'),
        'current_is_hr': current_is_hr  ,
        'synnex_experience': synnex_experience,
        'total_experience': total_experience,
    }

    return render(request, "profile/profile.html", context)

def cycle_progress(request):
    cycles = AppraisalCycle.objects.filter(status="Active")
    selected_cycle = None
    image_path = None

   
    cycle_images = {
        "semi-annual": "images/cycle_progress_1.png",
        "final year": "images/cycle_progress_2.png",
    }

    cycle_id = request.GET.get("cycle_id")

    if cycle_id:
        selected_cycle = AppraisalCycle.objects.get(id=cycle_id)
        image_path = cycle_images.get(selected_cycle.name, "images/default_cycle.png")

    return render(request, "masters/cycle_progress.html", {
        "cycles": cycles,
        "selected_cycle": selected_cycle,
        "image_path": image_path
    })

def get_all_subordinates(manager):
    subordinates = []
    direct = Employee.objects.filter(supervisor=manager)

    for emp in direct:
        subordinates.append(emp)
        subordinates.extend(get_all_subordinates(emp))

    return subordinates


@login_required
def manager_dashboard(request):
    departments = Department.objects.all()
    selected_department = None
    selected_manager = None
    managers = []
    employees_under_manager = []
    draft_forms = []
    
    active_cycle = AppraisalCycle.objects.filter(status="Active").first()

    department_id = request.GET.get("department")
    if department_id:
        selected_department = Department.objects.filter(id=department_id).first()
        if selected_department:
            managers = Employee.objects.filter(
                department=selected_department,
                role__role_name__in=["Manager", "Supervisor", "Supervisior"]
            ).select_related('role').order_by('role__role_name', 'first_name')

    manager_id = request.GET.get("manager")
    if manager_id and active_cycle:
        selected_manager = Employee.objects.filter(id=manager_id).first()
        if selected_manager:
            role_name = selected_manager.role.role_name.lower() if selected_manager.role else ""

            if role_name == "manager":
                dept_emps = Employee.objects.filter(department=selected_manager.department)\
                                           .exclude(id=selected_manager.id)
                subordinates = get_all_subordinates(selected_manager)
                employees_under_manager = list(set(list(dept_emps) + list(subordinates)))

            elif role_name in ["supervisor", "supervisior"]:
                employees_under_manager = list(
                    Employee.objects.filter(supervisor=selected_manager)
                )

            draft_forms = AppraisalForm.objects.filter(
                employee__in=employees_under_manager,
                appraisal_cycle=active_cycle,
                status="Draft"
            ).select_related("employee", "appraisal_cycle")

    return render(request, "masters/manager_dashboard.html", {
        "departments": departments,
        "selected_department": selected_department,
        "managers": managers,
        "selected_manager": selected_manager,
        "employees_under_manager": employees_under_manager,
        "draft_forms": draft_forms
    })
