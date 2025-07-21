from django.urls import path
from .views import manager_dashboard, user_dashboard, test, task_form_create, view_task, update_task, delete_task


urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name= 'manager_dashboard'),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('task-form-create/', task_form_create, name="task-form-create"),
    path('show-task/', view_task),
    path('update-task/<int:id>/', update_task, name='update'),
    path('delete-task/<int:id>/', delete_task, name='delete')
]