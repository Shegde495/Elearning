from django.forms import ModelForm
from .models import course
from .models import description,purchase

class CoursesForm(ModelForm):
    class Meta:
        model=course
        fields='__all__'
        exclude=['edited']

class ContentForm(ModelForm):
    class Meta:
        model=description
        fields='__all__'
        exclude=['name']

class Purchaseform(ModelForm):
    class Meta:
        model=purchase
        fields='__all__'