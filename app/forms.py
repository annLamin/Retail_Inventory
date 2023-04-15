from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),help_text="Required. Enter a valid email address")
    fname = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),help_text="Required. Enter Firstname")
    lname = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),help_text="Required. Enter Lastname")
    telephone = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),help_text="Required. Enter a valid telephone number")
    class Meta:
        model = User
        fields = ('email','fname','lname','telephone','password1','password2')
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'})
        }
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} already exists')


class UpdateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','password1','password2')
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
        }
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} already exists')

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user
     
class UpdateCashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = ('fname','lname','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
        }
    
class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = Sup_user
        fields = ('fname','lname','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
        }
    
class UpdateSellerForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = ('fname','lname','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
        }
class AddPayment(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount',)
        widgets = {
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
        }   

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('total_amount_paid','cust_name','cust_tel','cust_address')
        widgets = {
            'cust_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'cust_address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'cust_tel' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'total_amount_paid' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount Paid'}),
             }
class UpdateSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('cust_name','cust_tel','cust_address')
        widgets = {
            'cust_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'cust_address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'cust_tel' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
             }
#update_sale 
class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product_Group
        fields = ('product','sale','quantity','price')
        widgets = {
            'product' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product'}),
            'sale' : forms.TextInput(attrs={'class':'form-control','placeholder':'Sale'}),
            'quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Quantity'}),
            'price' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Unit Price'}),
     }

class UpdateSaleProductForm(forms.ModelForm):
    class Meta:
        model = Product_Group
        fields = ('quantity','price')
        widgets = {
            'quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Quantity'}),
            'price' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Unit Price'}),
     }

class DepositorForm(forms.ModelForm):
    class Meta:
        model = Depositor
        fields = ('fname','lname','address','telephone','description','balance')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Deposit'})
        }
class CashDepositorForm(forms.ModelForm):
    class Meta:
        model = CashDepositor
        fields = ('fname','lname','address','telephone','description','balance')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Deposit'})
        }

class UpdateDepositorForm(forms.ModelForm):
    class Meta:
        model = Depositor
        fields = ('fname','description','lname','address','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            }
class UpdateCashDepositorForm(forms.ModelForm):
    class Meta:
        model = CashDepositor
        fields = ('fname','description','lname','address','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            }


class UpdateSavingForm(forms.ModelForm):
    bank = forms.CharField(required=True),
    amount = forms.IntegerField(required=True),
    description = forms.CharField(required=True),
    image = forms.ImageField(required=True),

    class Meta:
        model = Saving
        fields = ('bank','amount','description', 'image',)
class UpdateRecordedSaleForm(forms.ModelForm):
    amount = forms.IntegerField(required=True),
   

    class Meta:
        model = RecordedSale
        fields = ('amount',)
    

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('fname','lname','address','description','telephone','balance')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Borrow'})
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salaries
        fields = ('staff','month','amount')
        widgets = {
            'staff' : forms.Select(),
            'month' : forms.TextInput(attrs={'class':'form-control','placeholder':'January'}),
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'})
        }
class SalForm(forms.ModelForm):
    class Meta:
        model = Salary_Transaction
        fields = ('month','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'month' : forms.TextInput(attrs={'class':'form-control','placeholder':'January'})
             }

class UpdateSalaryForm(forms.ModelForm):
    class Meta:
        model = Salaries
        fields = ('staff','month','amount')
        widgets = {
            'staff' : forms.Select(),
            'month' : forms.TextInput(attrs={'class':'form-control','placeholder':'Month'}),
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Borrow'})
        }

class UpdateBorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('fname','lname','description','address','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            }


class CashExpensesForm(forms.ModelForm):
    class Meta:
        model = CashExpenses
        fields = ('category','address','description','balance')
        widgets = {
            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Expenses'})
        }
class CashExpenseForm(forms.ModelForm):
    class Meta:
        model = CashExpenses_Transaction
        fields = ('description','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }
class UpdateCashExpensesForm(forms.ModelForm):
    class Meta:
        model = CashExpenses
        fields = ('category','address','description')
        widgets = {
            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'Category'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            # 'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Borrow'})
        }



class CashBorrowerForm(forms.ModelForm):
    class Meta:
        model = CashBorrower
        fields = ('fname','lname','address','description','telephone','balance')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Borrow'})
        }
class UpdateCashBorrowerForm(forms.ModelForm):
    class Meta:
        model = CashBorrower
        fields = ('fname','lname','description','address','telephone')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','brand', 'price','total_quantity','desc')
        widgets = {
            'category' : forms.Select(attrs={'class':'form-control custom-select','placeholder':'Product Category'}),
            'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'}),
            'brand' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product Brand'}),
            'price' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Price'}),
            'total_quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Total Quantity'}),
            'desc' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name',)
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Brand Name'}),
            }

class ExpenditureTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ('title', )
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Type of the expense...'}),
             
             }
class UpdateExpenditureTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ('title', )
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Type of the expense...'}),
             
             }

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('category','description','balance')
        widgets = {
            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            'balance' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Initial Expenses'})
        }


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expense_Transaction
        fields = ('description','amount')
        widgets = {
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }
class UpdateExpensesForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('category','description')
        widgets = {
            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'Category'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
            }




class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'brand','name','price','desc')
        widgets = {
            'category' : forms.Select(attrs={'class':'form-control custom-select','placeholder':'Product Category'}),
            'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'}),
            'brand' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product Brand'}),
            'price' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Price'}),
            'desc' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }
class UpdateBrandForm(forms.ModelForm):
    name = forms.CharField(required=True)
    
    class Meta:
        model = Brand
        fields = ('name',)
        
class ReceiptUpdateForm(forms.ModelForm):
    company = forms.CharField(required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    class Meta:
        model = Receipt
        fields = ('company','description','image')
class InvoiceUpdateForm(forms.ModelForm):
    company = forms.CharField(required=True)
    description = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    class Meta:
        model = Invoice
        fields = ('company','description','image')    

class ProductRestockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('total_quantity',)
        widgets = {
            'total_quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter quantity to add'})
        }

class AccountAuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','password')
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
            }
    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('Invalid Credentials')
    

class RestockForm(forms.Form):
    quantity = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Quantity to add'}))

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('description','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }

class CashDepositForm(forms.ModelForm):
    class Meta:
        model = CashTransaction
        fields = ('description','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }


# class DepositForm(forms.Form):
#     amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
class WithdrawForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))

class CashWithdrawForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))


class RepayForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))

class CashRepayForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))


class CashExpensesRepayForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))


class ExpensesRepayForm(forms.Form):
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])
    description = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrower_Transaction
        fields = ('description','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }
class CashBorrowForm(forms.ModelForm):
    class Meta:
        model = CashBorrower_Transaction
        fields = ('description','amount')
        widgets = {
           
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }

class CashExpenseForm(forms.ModelForm):
    class Meta:
        model = CashExpenses_Transaction
        fields = ('description','amount')
        widgets = {
            'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
            'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
             }

# class CashBorrowForm(forms.ModelForm):
#     class Meta:
#         model = CashBorrower_Transaction
#         fields = ('description','amount')
#         widgets = {
           
#             'amount' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}),
#             'description' : forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
#              }

# class BorrowForm(forms.Form):
#     amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Amount'}),validators=[MinValueValidator(0)])

class AuxillaryForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('fname','lname','telephone','address','salary')
        widgets = {
            'fname' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lname' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'telephone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Telephone'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'salary' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Salary'}),
        }  


class ReceiptForm(forms.ModelForm):
    company =  forms.CharField(required=True)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=True)
    class Meta:
        model = Receipt
        fields = ('company','description','image',)

class SavingForm(forms.ModelForm):
    bank =  forms.CharField(required=True)
    amount =  forms.IntegerField(required=True)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=True)
    class Meta:
        model = Saving
        fields = ('bank','amount','description','image',) 
class InvoiceForm(forms.ModelForm):
    company =  forms.CharField(required=True)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=True)
    class Meta:
        model = Invoice
        fields = ('company','description','image',)   

  
class StatementForm(forms.ModelForm):
    name = forms.CharField(required=True)
    subject=forms.Select()
    statement=forms.TextInput()
    class Meta:
        model = Statement
        fields = ('name','subject', 'statement')

class StatementUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    subject = forms.Select()
    statement = forms.TextInput()
    class Meta:
        model = Statement
        fields = ('name','subject','statement')

class SubjectForm(forms.ModelForm):
    name = forms.CharField(required=True)
    class Meta:
        model = Subject
        fields = ('name',)

class SubjectUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    class Meta:
        model = Subject
        fields = ('name',)



class RecordedSaleForm(forms.ModelForm):
    amount =  forms.IntegerField(required=True)

    class Meta:
        model = RecordedSale
        fields = ('amount',) 