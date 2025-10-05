from .models import Employee

def role_name(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            return {"role_name": employee.role.role_name.lower()}
        except Employee.DoesNotExist:
            return {"role_name": None}
    return {"role_name": None}

    