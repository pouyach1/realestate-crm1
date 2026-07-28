from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from customers.models import Customer
from properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # فقط برای superuser آمار رو بگیر
        if self.request.user.is_superuser:
            context['total_customers'] = Customer.objects.count()
            context['total_properties'] = Property.objects.count()
            context['available_properties'] = Property.objects.filter(status='available').count()
            context['sold_properties'] = Property.objects.filter(status='sold').count()
        return context