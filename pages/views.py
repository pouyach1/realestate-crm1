from django.views.generic import TemplateView, ListView
from properties.models import Property
from django.db.models import Q


class HomePageView(TemplateView):
    """صفحه اصلی"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.filter(
            status='available', is_featured=True
            ).select_related().prefetch_related('images').order_by('-created_at')[:6]
        context['urgent_properties'] = Property.objects.filter(status='available', is_urgent=True).order_by('-created_at')[:10]
        context['latest_properties'] = Property.objects.filter(status='available').order_by('-created_at')[:6]
        context['sold_properties'] = Property.objects.filter(status='sold').order_by('-created_at')[:6]
        context['popular_properties'] = Property.objects.filter(status='available').order_by('-view_count')[:6]
        return context


class SearchResultsView(ListView):
    """نتایج جستجوی عمومی"""
    model = Property
    template_name = 'search_results.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Property.objects.filter(status='available')
        q = self.request.GET.get('q', '')
        property_type = self.request.GET.get('property_type', '')
        price_range = self.request.GET.get('price_range', '')
        
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(address__icontains=q))
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if price_range:
            if price_range == '500m-1b':
                queryset = queryset.filter(price__gte=500000000, price__lte=1000000000)
            elif price_range == '1b-5b':
                queryset = queryset.filter(price__gte=1000000000, price__lte=5000000000)
            elif price_range == '5b-10b':
                queryset = queryset.filter(price__gte=5000000000, price__lte=10000000000)
            elif price_range == '10b+':
                queryset = queryset.filter(price__gte=10000000000)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_type'] = self.request.GET.get('property_type', '')
        context['selected_price'] = self.request.GET.get('price_range', '')
        context['total_results'] = self.get_queryset().count()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'