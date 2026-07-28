from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'آپارتمان'),
        ('villa', 'ویلا'),
        ('office', 'دفتر کار'),
        ('land', 'زمین'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'موجود'),
        ('sold', 'فروخته شده'),
        ('rented', 'اجاره داده شده'),
    ]
    
    title = models.CharField(max_length=300, verbose_name='عنوان')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='apartment', verbose_name='نوع ملک')
    price = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True, verbose_name='قیمت (تومان)')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='متراژ')
    yard_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='متراژ حیاط')
    storage = models.BooleanField(default=False, verbose_name='انباری')
    bedrooms = models.IntegerField(default=1, verbose_name='تعداد اتاق خواب')
    bathrooms = models.IntegerField(default=1, verbose_name='تعداد حمام')
    parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    has_elevator = models.BooleanField(default=False, verbose_name='آسانسور')
    floor_number = models.IntegerField(default=1, verbose_name='طبقه')
    total_floors = models.IntegerField(default=1, verbose_name='کل طبقات')
    address = models.TextField(verbose_name='آدرس')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='وضعیت')
    is_featured = models.BooleanField(default=False, verbose_name='نمایش در املاک ویژه')
    is_urgent = models.BooleanField(default=False, verbose_name='نمایش در فروش ویژه')
    view_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_price(self, user=None):
        if self.price is None or self.price == 0:
            return "تماس بگیرید"
        price = float(self.price)
        if user and user.is_authenticated:
            return self.formatted_price()
        else:
            if price < 500000000:
                return "زیر ۵۰۰ میلیون"
            elif price < 1000000000:
                return "۵۰۰ - ۱ میلیارد"
            elif price < 3000000000:
                return "۱ - ۳ میلیارد"
            elif price < 5000000000:
                return "۳ - ۵ میلیارد"
            elif price < 10000000000:
                return "۵ - ۱۰ میلیارد"
            else:
                return "بالای ۱۰ میلیارد"

    def formatted_price(self):
        if self.price is None:
            return "تماس بگیرید"
        price = float(self.price)
        if price == 0:
            return "تماس بگیرید"
        if price >= 1000000000:
            value = price / 1000000000
            if value == int(value):
                return f"{int(value)} میلیارد تومان"
            return f"{value:.1f} میلیارد تومان"
        elif price >= 1000000:
            value = price / 1000000
            return f"{int(value):,} میلیون تومان"
        else:
            return f"{int(price):,} تومان"

    def increase_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ملک'
        verbose_name_plural = 'املاک'
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name='ملک')
    image = models.ImageField(upload_to='properties/%Y/%m/%d/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'تصویر ملک'
        verbose_name_plural = 'تصاویر املاک'
    
    def __str__(self):
        return f"تصویر {self.property.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'
    
    def __str__(self):
        return f"{self.user.username} - {self.property.title}"