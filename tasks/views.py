from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

# Create your views here.
# ekhane jabotio logical function likhbo. means- task related joto kaj ache,sob ekhane hobe.


def manager_dashboard(request):
    #getting task count:
    # total_tasks = tasks.count()

    # completed_tasks = Task.objects.filter(status='COMPLETED').count()
    # in_progress_tasks = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_tasks = Task.objects.filter(status='PENDING').count()
    
    type = request.GET.get('type', 'all')     # 'all' ekti python er default jinis, 'type' dictionary te kichu thakle seta print hobe notuba 'all' print hobe.
    # print(type)
    

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))                                    
    )
    
    # Retrieving task data:
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    if type == 'all':
        tasks = base_query.all()            

    context = {
        'tasks' : tasks,
        'counts' : counts
        # 'total_task' : total_tasks,
        # 'completed_tasks' : completed_tasks,
        # 'in_progress_tasks' : in_progress_tasks,
        # 'pending_tasks' : pending_tasks
    }

    return render(request, "dashboard/manager-dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html") 

def test(request):
    names = ["Mahmud", "Ahamed", "John", "Mr. X"]
    count = 0
    for name in names:
        count += 1
    context = {
        "names": names,
        "age": 23,
        "count": count
    }
    return render(request, 'test.html', context)   

def task_form_create(request):
    # employeesV = Employee.objects.all()
    form = TaskModelForm()   # For 'GET' method
    task_detail_form = TaskDetailModelForm()
    print("GET request received")

    if request.method == 'POST':
        print("POST request received")
        form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST) # for taskdetailform

        if form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task_relation = task
            task_detail.save()
            
            messages.success(request, "Task created Successfully")
            return redirect('task-form-create')  # ('url_name')

            ''' For Django Form Data'''
            # data = form.cleaned_data

            # # Field-wise Data extract from cleaned data:
            # e_title = data.get('title')
            # e_description = data.get('description')
            # e_due_date = data.get('due_date')
            # e_assigned_to = data.get('assigned_to') # ekhane ekta list thakbe.
            
            # # Creating a new task
            # new_task = Task.objects.create(title=e_title, description=e_description, due_date=e_due_date)

            # # Assign employee to tasks:
            # for emp_id in e_assigned_to:
            #     empployee = Employee.objects.get(id=emp_id)
            #     new_task.assigned_to.add(empployee)
            
            # # Success message return:
            # return HttpResponse("Task Added successfully")
            
    context = {'form' : form, 'task_detail_form': task_detail_form}
    return render(request, "task_form.html", context)   




def update_task(request, id):
    # employeesV = Employee.objects.all()
    task = Task.objects.get(id=id)
    form = TaskModelForm(instance=task)   # For 'GET' method

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
        print("GET request received")

    if request.method == 'POST':
        print("POST request received")
        form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details) # for taskdetailform

        if form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task_relation = task
            task_detail.save()
            
            messages.success(request, "Task updated Successfully")
            return redirect('update', id)  # ('url_name')
            
    context = {'form' : form, 'task_detail_form': task_detail_form}
    return render(request, "task_form.html", context)   

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()

        messages.success(request, "Task deleted Successfully")
        return redirect('manager_dashboard') # ('url_name')
    else:
        messages.success(request, "Something went wrong")
        return redirect('manager_dashboard')# ('url_name')

def view_task(request):
# retrieve all data from tasks model:
    all_tasks = Task.objects.all()
    # return render(request, 'show_task.html', {"tasks": all_tasks})

# retrieve specific task from tasks model:
    task_3 = Task.objects.get(id=3)
    # return render(request, 'show_task.html', {"task3": task_3})
    
# Show the all pending tasks:
    p_tasks = Task.objects.filter(status='PENDING')
    #return render(request, 'show_task.html', {"pending_tasks": p_tasks})

# Show the tasks which due_date is today:
    tasks = Task.objects.filter(due_date=date.today())
    #return render(request, 'show_task.html', {"tasks": tasks})   

# Show the tasks whose priority is not low:
    tasks = TaskDetail.objects.exclude(priority='L')
    return render(request, 'show_task.html', {"tasks": tasks})

    # projects = Project.objects.annotate(
    #     num_task=Count('task')).order_by('num_task')
    # return render(request, "show_task.html", {"projects": projects})