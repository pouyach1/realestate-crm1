from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import LoginForm


class PersianUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'حداقل ۸ کاراکتر'}),
        error_messages={'required': 'لطفاً رمز عبور را وارد کنید.'}
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را دوباره وارد کنید'}),
        error_messages={'required': 'لطفاً تکرار رمز عبور را وارد کنید.'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {'username': 'نام کاربری'}
        error_messages = {
            'username': {
                'required': 'لطفاً نام کاربری را وارد کنید.',
                'unique': 'این نام کاربری قبلاً استفاده شده است.',
            },
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('دو رمز عبور وارد شده یکسان نیستند.')
        if len(password2) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ورود - Estate Basic'
        return context
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        # کاربر عادی → پنل کاربری | سوپر یوزر → داشبورد ادمین
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard:index')
        return reverse_lazy('dashboard:index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('pages:home')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = PersianUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')