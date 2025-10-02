from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AppraisalCycle, Employee, AppraisalForm

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.first_name.lower()

        # Ensure unique username
        counter = 1
        orig_username = username
        while User.objects.filter(username=username).exists():
            username = f"{orig_username}{counter}"
            counter += 1

        # Create linked User
        user = User.objects.create_user(
            username=username,
            password="default123",   # ⚠️ change on first login recommended
            first_name=instance.first_name,
            last_name=instance.last_name or "",
            email=instance.email,
        )
        instance.user = user
        instance.save()




@receiver(post_save, sender=AppraisalCycle)
def create_appraisal_forms_for_cycle(sender, instance, created, **kwargs):
    if instance.status == "Active":
        employees = Employee.objects.filter(status="Active")
        for emp in employees:
            AppraisalForm.objects.update_or_create(
                employee=emp,
                appraisal_cycle=instance,
                defaults={
                    "supervisor": emp.supervisor,
                    "department": emp.department,
                    "role": emp.role,
                }
            )

@receiver(post_save, sender=Employee)
def create_appraisal_form_for_new_employee(sender, instance, created, **kwargs):
    if created and instance.status == "Active":
        active_cycle = AppraisalCycle.objects.filter(status="Active").first()
        if active_cycle:
            AppraisalForm.objects.update_or_create(
                employee=instance,
                appraisal_cycle=active_cycle,
                defaults={
                    "supervisor": instance.supervisor,
                    "department": instance.department,
                    "role": instance.role,
                }
            )
