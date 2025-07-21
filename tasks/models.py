from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    # task_set = models.ManyToManyField(Task)
    # (same as taskdetail of Task. but many to many relation howyar karone ektu tofat ache. module 5.9 valo kore follow korte hobe.)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In_progress'),
        ('COMPLETED', 'Completed')
    ]

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE, 
        default=1,
        related_name='projects'
    )
    assigned_to = models.ManyToManyField(Employee,related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    # taskdetail = models.OneToOneField(TaskDetail, on_delete=models.CASCADE)

    # One to One relation er khettre Django automatically ei field create kore. eti TaskDetail er task_relation field er moto kaj kore. 
    # "Task model er object.taskdetail.priority" likhe command dile TaskDetail e access pabo jvabe "TaskDetail er object.task_relation.title" likhe command dile Task e access pai.

    # jodi Django er ei automatically deya ei field k use korte na cai,vinno kono name dite cai tahole TaskDetail er task_relation field e giye (related_name = 'details') likhe arekta attribute add korbo. jmon:  models.OneToOneField(Task, on_delete=models.CASCADE,related_name = 'details')
    
    
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    # task_id = models.CharField(max_length=200, primary_key=True)
    task_relation = models.OneToOneField(
        Task, 
        on_delete=models.CASCADE,
        related_name = 'details'
    )
    notes = models.TextField(blank=True, null=True)
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices = PRIORITY_OPTIONS, default='L')

    def __str__(self):
        return f"Details for Task {self.task_relation.title}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    # task_set = ....

    def __str__(self):
        return self.name
    
