from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from app.models import User
from app.models import *
# Register your models here.

class UserAccount(UserAdmin):
    list_display = ('email','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email',)
    readonly_fields = ('id','date_joined','last_login') 

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)

admin.site.register(User, UserAccount)

@admin.register(Sup_user)
class appAdmin(admin.ModelAdmin):
    list_display=['fname','lname','telephone']
    search_fields=['fname']

@admin.register(Product_Group)
class appAdmin(admin.ModelAdmin):
    list_display=['product','sale','quantity']

@admin.register(Salaries)
class appAdmin(admin.ModelAdmin):
    list_display=['staff','amount']
    # search_fields=['date']

@admin.register(Account)
class appAdmin(admin.ModelAdmin):
    list_display=['balance']
    search_fields=['balance']

@admin.register(Expense)
class appAdmin(admin.ModelAdmin):
    list_display=['category','description','balance','date']
    search_fields=['category']


@admin.register(Staff)
class appAdmin(admin.ModelAdmin):
    list_display=['fname','lname','telephone','address','salary']
    search_fields=['fname']

@admin.register(Cashier)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','telephone']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(Cash)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','telephone']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(Seller)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','telephone','type']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(Depositor)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','description','telephone','balance']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(Transaction)
class appAdmin(admin.ModelAdmin):
    list_display=['id','action','amount','date']
    search_fields=['id']
    list_filter=['id']
@admin.register(CashDepositor)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','description','telephone','balance']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(CashTransaction)
class appAdmin(admin.ModelAdmin):
    list_display=['id','action','amount','date']
    search_fields=['id']
    list_filter=['id']

@admin.register(Borrower)
class appAdmin(admin.ModelAdmin):
    list_display=['id','fname','lname','description', 'telephone','balance']
    search_fields=['fname']
    list_filter=['fname']

@admin.register(Receipt)
class appAdmin(admin.ModelAdmin):
    list_display=['id','date','company']
    search_fields=['company']

@admin.register(Saving)
class appAdmin(admin.ModelAdmin):
    list_display=['id','bank','amount']
    search_fields=['bank']

@admin.register(Invoice)
class appAdmin(admin.ModelAdmin):
    list_display=['id','date','company']
    search_fields=['company'] 

@admin.register(Borrower_Transaction)
class appAdmin(admin.ModelAdmin):
    list_display=['id','action','amount','date']
    search_fields=['id']
    list_filter=['id']

@admin.register(Sale)
class appAdmin(admin.ModelAdmin):
    list_display=['id','seller','total_price','actual_total_price','total_amount_paid','cust_name','cust_tel','cust_address','date']
    search_fields=['cust_name']
    list_filter=['cust_name']

@admin.register(Stock)
class appAdmin(admin.ModelAdmin):
    list_display=['id','product','seller','quantity']
    search_fields=['id']
    list_filter=['id']

@admin.register(Payment)
class appAdmin(admin.ModelAdmin):
    list_display=['id','sale','amount','date']
    search_fields=['id']
    list_filter=['id']


@admin.register(Product)
class appAdmin(admin.ModelAdmin):
    list_display=['id','category','name','brand','price','desc','total_quantity']
    search_fields=['name']
    list_filter=['name']

@admin.register(Brand)
class appAdmin(admin.ModelAdmin):
    list_display=['id', 'name']
    search_fields=['name']

@admin.register(ExpenseType)
class appAdmin(admin.ModelAdmin):
    list_display=['id', 'title']
    search_fields=['title']

@admin.register(CashExpenses)
class appAdmin(admin.ModelAdmin):
    list_display=['category','description','balance','date']
    search_fields=['category']

@admin.register(CashExpenses_Transaction)
class appAdmin(admin.ModelAdmin):
    list_display=['expense','amount','date']
    search_fields=['expense']

@admin.register(Expense_Transaction)
class appAdmin(admin.ModelAdmin):
    list_display=['expense','amount','date']
    search_fields=['expense']

@admin.register(CashAccount)
class appAdmin(admin.ModelAdmin):
    list_display=['balance']

@admin.register(Statement)
class appAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'subject']
    