from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from masters.models import Employee

class Command(BaseCommand):
    help = "Link Employee records with Django Users (by email)."

    def handle(self, *args, **kwargs):
        linked = 0
        created = 0

        for emp in Employee.objects.all():
            if emp.email:
                try:
                    user = User.objects.get(email=emp.email)
                except User.DoesNotExist:
                    # Create a User if not found
                    username = emp.email.split("@")[0]
                    user = User.objects.create_user(
                        username=username,
                        email=emp.email,
                        password="TempPass123",  # temporary password
                        first_name=emp.first_name,
                        last_name=emp.last_name,
                    )
                    created += 1

                # Link user to employee
                emp.user = user
                emp.save()
                linked += 1

        self.stdout.write(
            self.style.SUCCESS(f"Linked {linked} employees. Created {created} new users.")
        )
