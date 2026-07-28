from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.contrib import messages
from django.shortcuts import redirect
from .models import Customer
from .forms import CustomerForm
from .filters import CustomerFilter


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dashboard:index')


class CustomerListView(LoginRequiredMixin, SuperuserRequiredMixin, FilterView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    filterset_class = CustomerFilter
    paginate_by = 10


class CustomerCreateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')
    success_message = "مشتری با موفقیت ایجاد شد!"


class CustomerUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')
    success_message = "مشتری با موفقیت ویرایش شد!"


class CustomerDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "مشتری با موفقیت حذف شد!")
        return super().delete(request, *args, **kwargs)


class CustomerDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'