from django import forms
from .models import TodoItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['task', 'description', 'reminder_date', 'reminder_time', 'is_completed']

        wightsets = {
            'reminder_date': forms.DateInput(attrs={'type': 'date'}),
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }