from django.contrib import admin
from .models import Customer,Items,Order,OrderedItem,Feedback
# Register your models here.
admin.site.register(Customer)
admin.site.register(Items)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Feedback)