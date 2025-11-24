from django.urls import path
from . import views

app_name = "masters"

urlpatterns = [
    #Departments
    path("departments/", views.list_departments, name="list_departments"),
    path("departments/add/", views.add_department, name="add_department"),
    path("departments/<int:pk>/edit/", views.edit_department, name="edit_department"),
    path("departments/<int:pk>/delete/", views.delete_department, name="delete_department"),
    #Roles
    path("roles/", views.RoleList.as_view(), name="roles_list"),
    path("roles/add/", views.RoleCreate.as_view(), name="roles_add"),
    path("roles/<int:pk>/edit/", views.RoleUpdate.as_view(), name="roles_edit"),
    path("roles/<int:pk>/delete/", views.RoleDelete.as_view(), name="roles_delete"),
    # Appraisal Cycles
    path("cycles/", views.AppraisalCycleList.as_view(), name="cycles_list"),
    path("cycles/add/", views.AppraisalCycleCreate.as_view(), name="cycles_add"),
    path("cycles/<int:pk>/edit/", views.AppraisalCycleUpdate.as_view(), name="cycles_edit"),
    path("cycles/<int:pk>/delete/", views.AppraisalCycleDelete.as_view(), name="cycles_delete"),
    # Employees
    path("employees/", views.EmployeeList.as_view(), name="employees_list"),
    path("employees/add/", views.EmployeeCreate.as_view(), name="employees_add"),
    path("employees/<int:pk>/edit/", views.EmployeeUpdate.as_view(), name="employees_edit"),
    path("employees/<int:pk>/delete/", views.EmployeeDelete.as_view(), name="employees_delete"),
    # KRAs
    path("kras/", views.KRAList.as_view(), name="kras_list"),
    path("kras/add/", views.KRACreate.as_view(), name="kras_add"),
    path("kras/<int:pk>/edit/", views.KRAUpdate.as_view(), name="kras_edit"),
    path("kras/<int:pk>/delete/", views.KRADelete.as_view(), name="kras_delete"),
    # KPIs
    path("kpis/", views.KPIList.as_view(), name="kpis_list"),
    path("kpis/add/", views.KPICreate.as_view(), name="kpis_add"),
    path("kpis/<int:pk>/edit/", views.KPIUpdate.as_view(), name="kpis_edit"),
    path("kpis/<int:pk>/delete/", views.KPIDelete.as_view(), name="kpis_delete"),

    path("ratings/", views.rating_list, name="rating_list"),
    path("ratings/add/", views.rating_create, name="rating_create"),
    path("ratings/<int:pk>/edit/", views.rating_update, name="rating_update"),
    path("ratings/<int:pk>/delete/", views.rating_delete, name="rating_delete"),

    
    path("weightages/", views.weightage_list, name="weightage_list"),
    path("weightages/add/", views.weightage_create, name="weightage_create"),
    path("weightages/<int:pk>/edit/", views.weightage_update, name="weightage_update"),
    path("weightages/<int:pk>/delete/", views.weightage_delete, name="weightage_delete"),

    path("appraisal/", views.my_appraisal_redirect, name="my_appraisal"),
    path("appraisal/<int:appraisal_id>/", views.appraisal_form_view, name="appraisal_form"),
    path("appraisal/<int:appraisal_id>/add-objective/", views.add_objective, name="add_objective"),
    path("form/<int:appraisal_id>/", views.appraisal_form_view, name="appraisal_form_alt"),
    path("form/<int:appraisal_id>/add-objective/", views.add_objective, name="add_objective_alt"),
    path("reviews/", views.review_list_form, name="reviews_list"),
    path("team",views.team_appraisal_list, name="team_appraisal"),

    #profile
      path('employee-profile/', views.emp_profile, name='emp_profile'),
      path('employee-profile/<int:employee_id>/', views.emp_profile, name='emp_profile_view')

]
