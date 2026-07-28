from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field, HTML, Div
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    price = forms.DecimalField(required=False, label='قیمت (تومان)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'خالی = تماس بگیرید'}))
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'status', 'price', 'area', 'yard_area',
            'bedrooms', 'bathrooms', 'floor_number', 'total_floors',
            'parking', 'has_elevator', 'storage', 'address', 'description',
            'is_featured', 'is_urgent'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'yard_area': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'عنوان ملک',
            'property_type': 'نوع ملک',
            'status': 'وضعیت',
            'price': 'قیمت (تومان)',
            'area': 'متراژ بنا',
            'yard_area': 'متراژ حیاط',
            'bedrooms': 'اتاق خواب',
            'bathrooms': 'حمام',
            'floor_number': 'طبقه',
            'total_floors': 'کل طبقات',
            'parking': 'پارکینگ',
            'has_elevator': 'آسانسور',
            'storage': 'انباری',
            'address': 'آدرس',
            'description': 'توضیحات',
            'is_featured': 'املاک ویژه',
            'is_urgent': 'فروش ویژه',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="mb-3" style="font-weight: 700; color: #162233;"><i class="bi bi-info-circle me-2" style="color: #D4AE63;"></i>اطلاعات اصلی</h5>'),
            Row(
                Column(Field('title', css_class='form-control'), css_class='col-md-6'),
                Column(Field('property_type', css_class='form-select'), css_class='col-md-3'),
                Column(Field('status', css_class='form-select'), css_class='col-md-3'),
            ),
            Row(
                Column(Field('price', css_class='form-control'), css_class='col-md-4'),
                Column(Field('area', css_class='form-control'), css_class='col-md-4'),
                Column(Field('yard_area', css_class='form-control'), css_class='col-md-4'),
            ),
            HTML('<hr class="my-4">'),
            HTML('<h5 class="mb-3" style="font-weight: 700; color: #162233;"><i class="bi bi-house-door me-2" style="color: #D4AE63;"></i>ویژگی‌ها</h5>'),
            Row(
                Column(Field('bedrooms', css_class='form-control'), css_class='col-md-3'),
                Column(Field('bathrooms', css_class='form-control'), css_class='col-md-3'),
                Column(Field('floor_number', css_class='form-control'), css_class='col-md-3'),
                Column(Field('total_floors', css_class='form-control'), css_class='col-md-3'),
            ),
            Row(
                Column(Field('parking'), css_class='col-md-4'),
                Column(Field('has_elevator'), css_class='col-md-4'),
                Column(Field('storage'), css_class='col-md-4'),
            ),
            HTML('<hr class="my-4">'),
            HTML('<h5 class="mb-3" style="font-weight: 700; color: #162233;"><i class="bi bi-pin-map me-2" style="color: #D4AE63;"></i>موقعیت و توضیحات</h5>'),
            Field('address', css_class='form-control'),
            Field('description', css_class='form-control'),
            HTML('<hr class="my-4">'),
            HTML('<h5 class="mb-3" style="font-weight: 700; color: #162233;"><i class="bi bi-star me-2" style="color: #D4AE63;"></i>نمایش در سایت</h5>'),
            Row(
                Column(Field('is_featured'), css_class='col-md-6'),
                Column(Field('is_urgent'), css_class='col-md-6'),
            ),
            HTML('<hr class="my-4">'),
            Submit('submit', '💾 ذخیره ملک', css_class='btn-gold btn-lg w-100'),
        )


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیح عکس...'}),
        }