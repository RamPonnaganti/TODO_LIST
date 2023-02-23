from django import forms
from app1.models import TODO1

class Todoform(forms.Form):

    class Meta:
        model = TODO1
        fields = '__all__'