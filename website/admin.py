from django.contrib import admin
from .models import Record, Transaction, Payment, Product, Category, Transaction_Details

admin.site.register(Record)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Transaction_Details)






