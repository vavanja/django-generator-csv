from django import forms
from django.forms import ModelForm
from .models import DataSchema, Column


class UserLogin(forms.Form):
    pass


class DataSchemaForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = DataSchema
        # fields = "__all__"
        fields = ('name',)


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ('name', 'data_type', 'extra_args', 'order')
