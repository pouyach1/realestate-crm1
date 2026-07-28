from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from .models import Property, PropertyImage, Favorite
from .forms import PropertyForm, PropertyImageForm
from .filters import PropertyFilter


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dashboard:index')


# ========================================
# ADMIN VIEWS
# ========================================
class PropertyListView(LoginRequiredMixin, SuperuserRequiredMixin, FilterView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    filterset_class = PropertyFilter
    paginate_by = 9


class PropertyCreateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:list')
    success_message = "ملک با موفقیت ایجاد شد!"


class PropertyUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:list')
    success_message = "ملک با موفقیت ویرایش شد!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['image_form'] = PropertyImageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'upload_image' in request.POST:
            image_form = PropertyImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.property = self.object
                image.save()
                messages.success(request, 'تصویر آپلود شد!')
            return redirect('properties:update', pk=self.object.pk)
        return super().post(request, *args, **kwargs)


class PropertyDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('properties:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "ملک با موفقیت حذف شد!")
        return super().delete(request, *args, **kwargs)


# ========================================
# PUBLIC VIEWS
# ========================================
class PropertyDetailView(LoginRequiredMixin, DetailView):
    """جزئیات ملک - قابل دیدن برای همه کاربران لاگین شده"""
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_view()
        return response


# ========================================
# FAVORITES
# ========================================
class ToggleFavoriteView(LoginRequiredMixin, View):
    """افزودن/حذف علاقه‌مندی"""

    def post(self, request, *args, **kwargs):
        property_id = request.POST.get('property_id')
        property_obj = Property.objects.get(id=property_id)

        fav, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property_obj
        )

        if not created:
            fav.delete()
            return JsonResponse({'status': 'removed', 'message': 'از علاقه‌مندی‌ها حذف شد'})

        return JsonResponse({'status': 'added', 'message': 'به علاقه‌مندی‌ها اضافه شد'})


class FavoriteListView(LoginRequiredMixin, ListView):
    """لیست علاقه‌مندی‌های کاربر"""
    model = Favorite
    template_name = 'properties/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')