from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Form for creating and updating customers"""
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'request_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes about the customer...'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 234 567 890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'customer@example.com'}),
        }
        labels = {
            'name': 'نام',
            'phone': 'تلفن',
            'email': 'ایمیل',
            'request_type': 'نوع درخواست',
            'description': 'توضیحات',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Customer', css_class='btn-gold'))