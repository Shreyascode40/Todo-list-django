
from django.shortcuts import render
from .forms import TodoForm
from .models import TodoItem
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.

@login_required
def todo_list(request):
    print("Todo List View Accessed")

    todos = TodoItem.objects.all().order_by('-created_at')
    lists = todos.filter(is_completed=False)

    total_task = todos.count()
    completed_task = todos.filter(is_completed=True).count()
    print("TOTAL:", total_task)
    print("COMPLETED:", completed_task)


    return render(request, 'home.html', {
    'lists': lists,
    'total_task': total_task,
    'completed_task': completed_task
})
    



@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_create.html', {'form': form})

@login_required
def todo_update(request,pk):
    todo = get_object_or_404(TodoItem,pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo:todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_update.html', {'form': form})


@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(TodoItem,pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    return render(request, 'home')

@login_required
@require_POST
def todo_complete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)

    if not todo.is_completed:
        todo.is_completed = True
        todo.completed_at = now()
        todo.save()


    return redirect('todo:todo_list')
    


@login_required(login_url='account:login')
def tracker_view(request):
    today = now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year = today.year

    # ✅ TOTAL COMPLETED (USER-SPECIFIC)
    total_completed = TodoItem.objects.filter(
        user=request.user,
        is_completed=True
    ).count()

    # ✅ DAILY
    daily_done = TodoItem.objects.filter(
        user=request.user,
        is_completed=True,
        completed_at__date=today
    ).count()

    # ✅ WEEKLY
    weekly_done = TodoItem.objects.filter(
        user=request.user,
        is_completed=True,
        completed_at__date__gte=week_start
    ).count()

    # ✅ MONTHLY
    monthly_done = TodoItem.objects.filter(
        user=request.user,
        is_completed=True,
        completed_at__date__gte=month_start
    ).count()

    # ✅ YEARLY GRAPH (USER-SPECIFIC)
    yearly_data = (
        TodoItem.objects
        .filter(
            user=request.user,
            is_completed=True,
            completed_at__year=year
        )
        .annotate(month=TruncMonth('completed_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = [item['month'].strftime('%b') for item in yearly_data]
    counts = [item['count'] for item in yearly_data]

    # ✅ COMPLETED TASK HISTORY (USER-SPECIFIC)
    completed_tasks = TodoItem.objects.filter(
        user=request.user,
        is_completed=True
    ).order_by('-completed_at')

    context = {
        'daily_done': daily_done,
        'weekly_done': weekly_done,
        'monthly_done': monthly_done,
        'months': months,
        'counts': counts,
        'year': year,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'tracker.html', context)