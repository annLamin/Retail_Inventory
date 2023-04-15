from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password):
        user = self.create_user(
        email = self.normalize_email(email),
        password = password,)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email",max_length=254, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    hide_email = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Sup_user(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,unique=True)
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    telephone=models.IntegerField(blank=False)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Cashier(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,unique=True)
    fname = models.CharField( blank=False, max_length=30)
    lname=models.CharField(max_length=30,blank=False)
    telephone= models.IntegerField(blank=False)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Cash(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,unique=True)
    fname = models.CharField( blank=False, max_length=30)
    lname=models.CharField(max_length=30,blank=False)
    telephone= models.IntegerField(blank=False)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Seller(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,unique=True)
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    type_choice = (
        ('acc','Accessories'),
        ('mob','Mobile'),
        ('ele','Electronic')
    )
    type=models.CharField(max_length=30,choices=type_choice)
    telephone= models.IntegerField(blank=False)
    def __str__(self):
        return '%s %s  %s' % (self.fname, self.lname, self.user.email)
class Brand(models.Model):
    name=models.CharField(max_length=30,blank=False)
    def __str__(self):
        return '%s ' % (self.name,)
    
class Product(models.Model):
    prod_choice = (
        ('acc','Accessories'), 
        ('mob','Mobile'),
        ('ele','Electronics')
    )
    category=models.CharField(max_length=30, choices=prod_choice)
    name=models.CharField(max_length=30,blank=False)
    brand=models.CharField(max_length=30, null=True)
    price=models.IntegerField(blank=False)
    desc=models.TextField()
    total_quantity= models.IntegerField(blank=False)
    def __str__(self):
        return '%s is of type %s' % (self.name, self.category)




class Stock(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=False)
    def __str__(self):
        return '%s' % (self.quantity)
    
class Sale(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    total_price = models.IntegerField( blank=False)
    actual_total_price = models.IntegerField( blank=False, default=0)
    total_amount_paid = models.IntegerField( blank=False)
    cust_name = models.CharField(max_length=30,blank=False)
    cust_tel = models.IntegerField(blank=False)
    cust_address = models.CharField(max_length=30, blank=False)
    date=models.DateTimeField(blank=False)
    view_counts = models.PositiveIntegerField(default=0)
    def __str__(self):
        return '%s  made a sale to %s' % (self.seller,self.cust_name)
    
   
class Payment(models.Model):
    sale = models.ForeignKey( Sale, on_delete=models.CASCADE)
    amount=models.IntegerField(blank=False)
    desc=models.CharField(max_length=100, null=True)
    total_amount=models.IntegerField(blank=False)
    balance=models.IntegerField(blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return 'payment of %s on %s' % (self.amount, self.date,)

class ExpenseType(models.Model):
    title = models.CharField(max_length=30, blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return self.title

class Expense(models.Model):
    category = models.CharField( blank=False, max_length=60)
    description=models.CharField(max_length=30, blank=False)
    balance = models.IntegerField(blank=False)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s recieved %s' % (self.category, self.balance)

class Expense_Transaction(models.Model):
    transc_choice = (
        ('Expense','Expense'),
        ('Payment','Payment')
    )
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField( max_length=50, blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.expense,self.action, self.amount)   


class Saving(models.Model):
    bank =  models.CharField(max_length=100, blank=False)
    amount =  models.IntegerField(blank=False)
    description = models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='bank')


class Receipt(models.Model):
    company =  models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='receipt')

class Invoice(models.Model):
    company =  models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='invoice')

class Product_Group(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey( Product, on_delete=models.CASCADE)
    sale = models.ForeignKey( Sale, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False, default=0)

class Depositor(models.Model):
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    description=models.CharField(max_length=50,blank=False)
    telephone=models.IntegerField(blank=False)
    balance =models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class CashDepositor(models.Model):
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    description=models.CharField(max_length=50,blank=False)
    telephone=models.IntegerField(blank=False)
    balance =models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Transaction(models.Model):
    transc_choice = (
        ('Withdraw','Withdraw'),
        ('Deposit','Deposit')
    )
    depositor=models.ForeignKey(Depositor,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField(max_length=50,blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.depositor,self.action, self.amount)   

class CashTransaction(models.Model):
    transc_choice = (
        ('Withdraw','Withdraw'),
        ('Deposit','Deposit')
    )
    depositor=models.ForeignKey(CashDepositor,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField(max_length=50,blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.depositor,self.action, self.amount)   


class Borrower(models.Model):
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    description=models.CharField(max_length=50,blank=False)
    telephone=models.IntegerField(blank=False)
    balance =models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class CashExpenses(models.Model):
    category=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    description=models.CharField(max_length=50,blank=False)
    balance =models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.category, self.address)

class CashExpenses_Transaction(models.Model):
    transc_choice = (
        ('Expense','Expense'),
        ('Payment','Payment')
    )
    expense=models.ForeignKey(CashExpenses,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField( max_length=50, blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.expense,self.action, self.amount)   


class CashBorrower(models.Model):
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    description=models.CharField(max_length=50,blank=False)
    telephone=models.IntegerField(blank=False)
    balance =models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Borrower_Transaction(models.Model):
    transc_choice = (
        ('Payment','Payment'),
        ('Borrow','Borrow')
    )
    borrower=models.ForeignKey(Borrower,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField( max_length=50, blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.borrower,self.action, self.amount)   

class CashBorrower_Transaction(models.Model):
    transc_choice = (
        ('Payment','Payment'),
        ('Borrow','Borrow')
    )
    borrower=models.ForeignKey(CashBorrower,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    description=models.CharField( max_length=50, blank=False)
    date=models.DateTimeField(blank=False)
    def __str__(self):
        return '%s made a %s of %s' % (self.borrower,self.action, self.amount)   

class Staff(models.Model):
    fname=models.CharField(max_length=30,blank=False)
    lname=models.CharField(max_length=30,blank=False)
    address=models.CharField(max_length=50,blank=False)
    telephone=models.IntegerField(blank=False)
    salary =models.IntegerField(blank=False)  

    def __str__(self):
        return '%s %s' % (self.fname, self.lname)
class Salaries(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE )
    amount= models.IntegerField(blank=False)
    month=models.CharField(max_length=50,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s recieved %s' % (self.staff, self.amount)

class Salary_Transaction(models.Model):
    transc_choice = (
        ('Payment','Payment'),
        ('Refund','Refund')
    )
    salary=models.ForeignKey(Salaries,on_delete=models.CASCADE)
    action=models.CharField(max_length=45,choices = transc_choice)
    amount=models.IntegerField(blank=False)
    month=models.CharField( max_length=50, blank=False)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s made a %s of %s' % (self.salary,self.action, self.amount)   


class Account(models.Model):
    balance = models.IntegerField(blank=False)
    def __str__(self):
        return '%s' % (self.balance)
 
class CashAccount(models.Model):
    balance = models.IntegerField(blank=False)
    def __str__(self):
        return '%s' % (self.balance)

class RecordedSale(models.Model):
    cash =  models.ForeignKey(Cash, on_delete=models.CASCADE)
    amount =  models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return '%s' % (self.name)
class Statement(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    statement = models.TextField(max_length=1000)
