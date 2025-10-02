from django import forms
from .models import KPI, Department,Role
from .models import AppraisalCycle , Employee , KRA
from . import models
from django.db.models import Sum
from django import forms
from .models import RatingMaster, WeightageMaster
from django.forms import inlineformset_factory

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "division", "country", "state", "city"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "division": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control", "id": "country-select"}),
            "state": forms.Select(attrs={"class": "form-control", "id": "state-select"}),
            "city": forms.Select(attrs={"class": "form-control", "id": "city-select"}),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["role_name", "description"]
        widgets = {
            "role_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class AppraisalCycleForm(forms.ModelForm):
    class Meta:
        model = AppraisalCycle
        fields = ["name", "year", "start_date", "end_date", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "department",
            "role",
            "supervisor",
            "status",
        ]
        widgets = {
            "employee_id": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "supervisor": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

from django import forms
from django.db.models import Sum
from .models import KRA

class KRAForm(forms.ModelForm):
    class Meta:
        model = KRA
        fields = ["department", "kra_name", "weightage"]
        widgets = {
            "department": forms.Select(attrs={"class": "form-control"}),
            "kra_name": forms.TextInput(attrs={"class": "form-control"}),
            "weightage": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dept = cleaned_data.get("department")
        weightage = cleaned_data.get("weightage")

        if dept and weightage is not None:
            existing_total = (
                KRA.objects.filter(department=dept)
                .exclude(pk=self.instance.pk)  # exclude itself on update
                .aggregate(total=Sum("weightage"))["total"]
                or 0
            )
            if existing_total + weightage > 100:
                raise forms.ValidationError(
                    f"Total KRA weightage for {dept} cannot exceed 100% (already at {existing_total}%)."
                )
        return cleaned_data
    
class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ["kra", "name", "description", "weightage"]
        widgets = {
            "kra": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "weightage": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }




from django import forms
from .models import RatingMaster, WeightageMaster


class RatingMasterForm(forms.ModelForm):
    class Meta:
        model = RatingMaster
        fields = ["appraisal_cycle", "current_year", "rating_score",]
        widgets = {
            "appraisal_cycle": forms.Select(attrs={"class": "form-control"}),
            "current_year": forms.TextInput(attrs={"class": "form-control", "placeholder": "2025-2026"}),
            "rating_score": forms.NumberInput(attrs={"class": "form-control"}),
            "rating": forms.TextInput(attrs={"class": "form-control"}),
        }

class WeightageMasterForm(forms.ModelForm):
    class Meta:
        model = WeightageMaster
        fields = ["appraisal_cycle", "current_year", "weightage_employee", "weightage_supervisor", "weightage_manager1", "weightage_manager2"]
        widgets = {
            "appraisal_cycle": forms.Select(attrs={"class": "form-control"}),  
            "current_year": forms.TextInput(attrs={"class": "form-control", "placeholder": "2025-2026"}),
            "weightage_employee": forms.NumberInput(attrs={"class": "form-control"}),
            "weightage_supervisor": forms.NumberInput(attrs={"class": "form-control"}),
            "weightage_manager1": forms.NumberInput(attrs={"class": "form-control"}),
            "weightage_manager2": forms.NumberInput(attrs={"class": "form-control"}),
        }



from django import forms
from .models import RatingMaster, WeightageMaster


class RatingMasterForm(forms.ModelForm):
    class Meta:
        model = RatingMaster
        fields = ["appraisal_cycle", "current_year", "rating_score",]
        widgets = {
            "appraisal_cycle": forms.TextInput(attrs={"class": "form-control"}),
            "current_year": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2025-2026"}),
            
            "rating_score": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "100"}),
        }

    def clean_rating_score(self):
        score = self.cleaned_data.get("rating_score")
        if score < 0 or score > 100:
            raise forms.ValidationError("Rating score must be between 0 and 100.")
        return score

    def save(self, commit=True):
        instance = super().save(commit=False)
        score = instance.rating_score

        
        if 80 <= score <= 100:
            instance.rating = "A"
        elif 60 <= score <= 79:
            instance.rating = "B+"
        elif 40 <= score <= 59:
            instance.rating = "B"
        elif 20 <= score <= 39:
            instance.rating = "C"
        else:
            instance.rating = "D"

        if commit:
            instance.save()
        return instance

class WeightageMasterForm(forms.ModelForm):
    class Meta:
        model = WeightageMaster
        fields = [
            "appraisal_cycle", "current_year", "appraisal_id",
            "weightage_employee", "weightage_supervisor",
            "weightage_manager1", "weightage_manager2"
        ]



from .models import AppraisalForm
from django import forms

class HrAppraisalForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["user", "first_name", "last_name", "department"]
        widgets = {
            "user": forms.TextInput(attrs={"readonly": "readonly"}),
            "first_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "last_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "department": forms.TextInput(attrs={"readonly": "readonly"}),
        }



from django import forms
from .models import EmployeeObjective, EmployeeKPI

class EmployeeObjectiveForm(forms.ModelForm):
    class Meta:
        model = EmployeeObjective
        fields = ["objective", "weightage"]


class EmployeeKPIForm(forms.ModelForm):
    class Meta:
        model = EmployeeKPI
        fields = ["name", "target", "achieved", "remarks"]

EmployeeKPIFormSet = inlineformset_factory(
    EmployeeObjective, EmployeeKPI,
    form=EmployeeKPIForm,
    extra=1, can_delete=True
)