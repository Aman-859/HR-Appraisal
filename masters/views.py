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
from .models import Department, Country, State, City
from .forms import DepartmentForm
from .models import Employee, KRA, KPI
from .models import AppraisalCycle, Employee
from .models import AppraisalCycle, AppraisalForm, Employee, KRA
from .models import EmployeeObjective
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
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