from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone
# try
from django.views.generic import ListView
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import*
from .forms import *
from .decorators import allowed_users
from datetime import datetime
import random
from django.core.cache import cache
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('/login/')

def cashier_mob_sales(request):
    return redirect('/cashier_mobile_sales/')

def cashier_ele_sales(request):
    return redirect('/cashier_electronic_sales/')

def cashier_acc_sales(request):
    return redirect('/cashier_accessories_sales/')

def admin_all_sales(request):
    return redirect('/admin_sales_reports/')

def seller_mob_sales(request):
    return redirect('/view_mobile_sales/')

def seller_ele_sales(request):
    return redirect('/view_electronics_sales/')

def seller_acc_sales(request):
    return redirect('/view_accessories_sales/')

def del_mob_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/mobile_sale/')

def del_mobinv_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/create_mobile_invoice/')

def del_ele_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/electronics_sale/')

def del_eleinv_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/create_electronics_invoice/')

def del_acc_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/accessories_sale/')

def del_accinv_ses(request):
    if 'products' in request.session:
        del request.session['products']
        del request.session['total_p']
        del request.session['act_total_p']
    return redirect('/create_accessories_invoice/')

def confirm_delete_admin(request,uid):
    admin = get_object_or_404(Sup_user,pk=uid)
    if admin == request.user.admin:
        messages.warning(request, "!!!Error!!! You cannot delete the currently logged in user") 
    else:
        user = get_object_or_404(User,email=admin.user.email)
        user.is_active = False
        user.save()
        messages.success(request, 'Success!! User Deleted Sucessfully')

def confirm_delete_cashier(request,uid):
    cashier = get_object_or_404(Cashier,pk=uid)
    user = User.objects.get(email=cashier.user.email)
    user.is_active = False
    user.save()
    messages.success(request, 'Success!! User Deleted Sucessfully')

def confirm_delete_aux(request,uid):
    aux = get_object_or_404(Staff,pk=uid)
    total_salary = 0
    for pay in Salaries.objects.filter(staff=aux):
        total_salary += pay.amount
    reciepient = aux.fname + ' ' + aux.lname
    Expense.objects.create(reciepient=reciepient,desc='Total salary paid to deleted staff',amount=total_salary,date=timezone.now())                
    aux.delete()
    messages.success(request, 'Success!! User Deleted Sucessfully')

def confirm_delete_exp(request,eid):
    exp = get_object_or_404(Expense,pk=eid)
    acc = Account.objects.all()[0]
    acc.balance += exp.balance
    acc.save()
    exp.delete()
    messages.success(request, 'Success!! Expenditure Deleted Sucessfully')


def confirm_delete_bor(request,bid):
    bor = get_object_or_404(Borrower,pk=bid) 
    acc = Account.objects.all()[0]
    acc.balance += bor.balance
    acc.save()
    bor.delete()
    messages.success(request, 'Success!! Borrower Deleted Sucessfully')

def confirm_delete_sal(request,sid):
    sal = get_object_or_404(Salaries,pk=sid) 
    sal.delete()
    messages.success(request, 'Success!! Salary Deleted Sucessfully')
  

def confirm_delete_cashbor(request,bid):
    bor = get_object_or_404(CashBorrower,pk=bid) 
    acc = CashAccount.objects.all()[0]
    acc.balance += bor.balance
    acc.save()
    bor.delete()
    messages.success(request, 'Success!! Borrower Deleted Sucessfully')

def confirm_delete_cashexps(request,eid):
    exp = get_object_or_404(CashExpenses,pk=eid) 
    acc = CashAccount.objects.all()[0]
    acc.balance += exp.balance
    acc.save()
    exp.delete()
    messages.success(request, 'Success!! Expenses Deleted Sucessfully')
  


def confirm_delete_sale(request,sid):
    sale = get_object_or_404(Sale,pk=sid) 
    acc = Account.objects.all()[0]
    acc.balance -= sale.total_price
    acc.save()
    sale.delete()
    messages.success(request, 'Success!! Sale Deleted Sucessfully')


def confirm_delete_dep(request,did):
    dep = get_object_or_404(Depositor,pk=did) 
    acc = Account.objects.all()[0]
    acc.balance -= dep.balance
    acc.save()
    dep.delete()
    messages.success(request, 'Success!! Depositor Deleted Sucessfully')

def confirm_delete_cashdep(request,did):
    dep = get_object_or_404(CashDepositor,pk=did) 
    acc = CashAccount.objects.all()[0]
    acc.balance -= dep.balance
    acc.save()
    dep.delete()
    messages.success(request, 'Success!! Depositor Deleted Sucessfully')
    
def confirm_delete_reciept(request,rid):
    receipt = get_object_or_404(Receipt,pk=rid)
    receipt.delete()
    
    messages.success(request, 'Success!! Reciept Deleted Sucessfully')

def confirm_delete_invoice(request,iid):
    invoice = get_object_or_404(Invoice,pk=iid)
    invoice.delete()
    
    messages.success(request, 'Success!! Invioce Deleted Sucessfully')

def confirm_delete_statement(request,sid):
    statement = get_object_or_404(Statement,pk=sid)
    statement.delete()
    
    messages.success(request, 'Success!! Statement Deleted Sucessfully')

def confirm_delete_brand(request,bid):
    brand = get_object_or_404(Brand,pk=bid)
    brand.delete()
    
    messages.success(request, 'Success!! Brand Deleted Sucessfully')
 

def confirm_delete_seller(request,uid):
    seller = get_object_or_404(Seller,pk=uid)
    user = get_object_or_404(User,email=seller.user.email)
    user.is_active = False
    user.save()
    messages.success(request, 'Success!! User Deleted Sucessfully')

def confirm_delete_cashsale(request,sid):
    sale = get_object_or_404(RecordedSale,pk=sid) 
    acc = CashAccount.objects.all()[0]
    acc.balance -= sale.amount
    acc.save()
    sale.delete()
    messages.success(request, 'Success!! Depositor Deleted Sucessfully')
  
def login_view(request):
    if not Account.objects.all().exists():
        Account.objects.create(balance=0)
    login_form = AccountAuthenticationForm()
    message = ''
    user = request.user
    if request.method == 'POST':
        login_form = AccountAuthenticationForm(request.POST)
        if not user.is_authenticated:
            if login_form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(request,email=email,password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        if Sup_user.objects.filter(user__email=email).exists():
                            return redirect('/admin_home/')
                        elif Cashier.objects.filter(user__email=email).exists():
                            return redirect('/cashier_home/')
                        elif Cash.objects.filter(user__email=email).exists():
                            return redirect('/cash_home/')
                        elif Seller.objects.filter(user__email=email,type='acc').exists():
                            return redirect('/accessories_home/')
                        elif Seller.objects.filter(user__email=email,type='mob').exists():
                            return redirect('/mobile_home/')
                        elif Seller.objects.filter(user__email=email,type='ele').exists():
                            return redirect('/electronics_home/')
                    else:
                        message = 'You are not allowed'
        else:
            if Sup_user.objects.filter(user=user).exists():
                loguser = get_object_or_404(Sup_user,user=user)
                logname = loguser.user.email
                messages.warning(request, f"!!!Logged in as {logname}!!! Logout to signin as another user!!!")
                return redirect('/admin_home/')
            elif Cashier.objects.filter(user=user).exists():
                loguser = get_object_or_404(Cashier,user=user)
                logname = loguser.user.email
                messages.warning(request, f"!!!Logged in as {logname}!!! Logout to signin as another user!!!")
                return redirect('/cashier_home/')
            elif Cash.objects.filter(user=user).exists():
                loguser = get_object_or_404(Cash,user=user)
                logname = loguser.user.email
                messages.warning(request, f"!!!Logged in as {logname}!!! Logout to signin as another user!!!")
                return redirect('/cash_home/')
            elif Seller.objects.filter(user=user).exists():
                sel = get_object_or_404(Seller,user=user)
                loguser = get_object_or_404(Seller,user=user)
                logname = loguser.user.email
                messages.warning(request, f"!!!Logged in as {logname}!!! Logout to signin as another user!!!")
                if sel.type == 'acc':
                    return redirect('/accessories_home/')
                elif sel.type == 'mob':
                    return redirect('/mobile_home/')
                elif sel.type == 'ele':
                    return redirect('/electronics_home/')
    return render(request,'login.html',{'message':message,'login_form':login_form,'title':'Login'})
# sales views

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def mobile_home(request):
    user_name = request.user.seller
    stocks = Stock.objects.filter(seller=user_name)
    return render(request, 'sales/mobile.html', {'stocks':stocks,'user_name':user_name,'title': 'Home'})

def search_status(request):

    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            statuss = Product.objects.filter(status__contains = search_text)
        else:
            statuss = []

        return render(request, 'ajax_search.html', {'statuss':statuss})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def view_mobile_sale_product(request,sid):
    user_name = request.user.seller
    mob_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'sales/mobile_sale_products.html',{'mob_sales_prod':mob_sales_prod,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def create_accessories_invoice(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
    else:
        select_prod = {}
        total_price = 0
    acc_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            if int(quantity) > 0:
                if int(sell_price) > 0:
                    if 'products' in request.session:
                        if product_id in request.session['products'].keys():
                            temp = request.session['products']
                            request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                        val = request.session['products']
                        val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                        request.session['products'] = val
                        val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                        request.session['total_p'] = val2
                        total_price = request.session['total_p']
                    else:
                        request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                        select_prod = request.session['products']
                        request.session['total_p'] = int(sell_price)*int(quantity)
                        total_price = request.session['total_p']
                else:
                    messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            if select_prod:
                for pro in select_prod:
                    product = get_object_or_404(Product,pk=int(pro))
                cust_name = request.POST['cust_name']
                invoice_num = random.randint(0,1000000)
                date = timezone.now()
                del request.session['products']
                return render(request, 'sales/view_accessories_invoice.html', {'total_price':total_price,'select_prod':select_prod,'invoice_num':invoice_num,'date':date,'cust_name':cust_name,'products':products,'user_name':user_name,'acc_form':acc_form,'title': 'Home'})
            else:
                messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/create_accessories_invoice.html', {'total_price':total_price,'select_prod':select_prod,'products':products,'user_name':user_name,'acc_form':acc_form,'title': 'View Sales'})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def create_mobile_invoice(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
    else:
        select_prod = {}
        total_price = 0
    mob_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            if int(quantity) > 0:
                if int(sell_price) > 0:
                    if 'products' in request.session:
                        if product_id in request.session['products'].keys():
                            temp = request.session['products']
                            request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                        val = request.session['products']
                        val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                        request.session['products'] = val
                        val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                        request.session['total_p'] = val2
                        total_price = request.session['total_p']
                    else:
                        request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                        select_prod = request.session['products']
                        request.session['total_p'] = int(sell_price)*int(quantity)
                        total_price = request.session['total_p']
                else:
                    messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            if select_prod:
                for pro in select_prod:
                    product = get_object_or_404(Product,pk=int(pro))
                cust_name = request.POST['cust_name']
                invoice_num = random.randint(0,1000000)
                date = timezone.now()
                del request.session['products']
                return render(request, 'sales/view_mobile_invoice.html', {'total_price':total_price,'select_prod':select_prod,'invoice_num':invoice_num,'date':date,'cust_name':cust_name,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'Home'})
            else:
                messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/create_mobile_invoice.html', {'total_price':total_price,'select_prod':select_prod,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def create_electronics_invoice(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
    else:
        select_prod = {}
        total_price = 0
    ele_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            if int(quantity) > 0:
                if int(sell_price) > 0:
                    if 'products' in request.session:
                        if product_id in request.session['products'].keys():
                            temp = request.session['products']
                            request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                        val = request.session['products']
                        val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                        request.session['products'] = val
                        val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                        request.session['total_p'] = val2
                        total_price = request.session['total_p']
                    else:
                        request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                        select_prod = request.session['products']
                        request.session['total_p'] = int(sell_price)*int(quantity)
                        total_price = request.session['total_p']
                else:
                    messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            if select_prod:
                for pro in select_prod:
                    product = get_object_or_404(Product,pk=int(pro))
                cust_name = request.POST['cust_name']
                invoice_num = random.randint(0,1000000)
                date = timezone.now()
                del request.session['products']
                return render(request, 'sales/view_electronics_invoice.html', {'total_price':total_price,'select_prod':select_prod,'invoice_num':invoice_num,'date':date,'cust_name':cust_name,'products':products,'user_name':user_name,'ele_form':ele_form,'title': 'Home'})
            else:
                messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/create_electronics_invoice.html', {'total_price':total_price,'select_prod':select_prod,'products':products,'user_name':user_name,'ele_form':ele_form,'title': 'View Sales'})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def mobile_sale(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
        act_total_price = request.session['act_total_p']
    else:
        select_prod = {}
        total_price = 0
        act_total_price = 0
    mob_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
            if int(quantity) > 0:
                if int(quantity) <= tar_prod.quantity:
                    if int(sell_price) > 0:
                        if 'products' in request.session:
                            if product_id in request.session['products'].keys():
                                temp = request.session['products']
                                request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                                request.session['act_total_p'] -= (int(temp[product_id][0])*int(product.price))
                            val = request.session['products']
                            val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                            request.session['products'] = val
                            val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                            val3 = request.session['act_total_p'] + (int(product.price)*int(quantity))
                            request.session['total_p'] = val2
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = val3
                            act_total_price = request.session['act_total_p']
                        else:
                            request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                            select_prod = request.session['products']
                            request.session['total_p'] = int(sell_price)*int(quantity)
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = int(product.price)*int(quantity)
                            act_total_price = request.session['act_total_p']
                    else:
                        messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
                else:
                    messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                if select_prod:
                    bal = total_price - total_amount_paid
                    if int(total_amount_paid) >= 0:
                        if bal < 0:
                            messages.warning(request, f'!!!ERROR!!! The amount paid is more than the total price.')
                        else:
                            for pro in select_prod:
                                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=int(pro))
                                tar_prod.quantity = F('quantity') - int(select_prod[pro][0]) 
                                tar_prod.save()
                            sale = Sale.objects.create(seller=user_name,total_price=total_price,actual_total_price=act_total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address,date=timezone.now())
                            Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                            for prod in select_prod:
                                product = get_object_or_404(Product,pk=int(prod))
                                quantity = int(select_prod[prod][0])
                                amt = int(select_prod[prod][3]) 
                                Product_Group.objects.create(sale=sale,product=product,quantity=quantity,price=amt)
                            acc = Account.objects.all()[0]
                            acc.balance += int(total_amount_paid)
                            acc.save()
                            del request.session['products']
                            messages.success(request, 'Success!! Sale made sucessfully')
                            return redirect('/mobile_home/')
                    else:
                        messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
                else:
                        messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/mobile_sale.html', {'total_price':total_price,'select_prod':select_prod,'products':products,
    'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})


# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['mobile'])
# def view_mobile_sales(request):
#     user_name = request.user.seller
#     mob_sales= Sale.objects.filter(seller= user_name)
#     val_set = ''
#     total_amount = 0
#     total_price = 0
#     sale_no = 0
#     if request.method == 'POST': 
#         start = request.POST['startdate']
#         end = request.POST['enddate']
#         val_set = f'All Sales from {start} to {end}'
#         mob_sales= Sale.objects.filter(seller= user_name,date__date__lte=end,date__date__gte=start)
#         for sale in mob_sales:
#             total_price += sale.total_price
#             total_amount += sale.total_amount_paid
#         sale_no = mob_sales.count()
#     return render(request, 'sales/view_mobile_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'mob_sales':mob_sales,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def edit_mobile_sale(request,sid):
    user_name = request.user.seller
    sal = get_object_or_404(Sale,pk=sid)
    mob_form = UpdateSaleForm(instance=sal)
    if request.method == 'POST':
        mob_form = UpdateSaleForm(request.POST,instance=sal)
        if mob_form.is_valid():
            mob_form.save()
            messages.success(request, 'Success!! Customer details updated sucessfully')
            return redirect('/view_mobile_sales/')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_mobile_sale.html', {'mob_form':mob_form,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def edit_electronic_sale(request,sid):
    user_name = request.user.seller
    sal = get_object_or_404(Sale,pk=sid)
    ele_form = UpdateSaleForm(instance=sal)
    if request.method == 'POST':
        ele_form = UpdateSaleForm(request.POST,instance=sal)
        if ele_form.is_valid():
            ele_form.save()
            messages.success(request, 'Success!! Customer details updated sucessfully')
            return redirect('/view_electronics_sales/')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_electronics_sale.html', {'ele_form':ele_form,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def edit_accessories_sale(request,sid):
    user_name = request.user.seller
    sal = get_object_or_404(Sale,pk=sid)
    acc_form = UpdateSaleForm(instance=sal)
    if request.method == 'POST':
        acc_form = UpdateSaleForm(request.POST,instance=sal)
        if acc_form.is_valid():
            acc_form.save()
            messages.success(request, 'Success!! Customer details updated sucessfully')
            return redirect('/view_accessories_sales/')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_accessories_sale.html', {'acc_form':acc_form,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def edit_mobile_sale_product(request,pid):
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    sal = get_object_or_404(Product_Group,pk=pid)
    salee = get_object_or_404(Product_Group,pk=pid)
    sid = sal.sale.id
    mob_form = UpdateSaleProductForm(instance=sal)
    if request.method == 'POST':
        mob_form = UpdateSaleProductForm(request.POST,instance=sal)
        if mob_form.is_valid():
            quantity = mob_form.cleaned_data['quantity']
            price = mob_form.cleaned_data['price']
            prod = request.POST['prod']
            product = get_object_or_404(Product,pk=int(prod))
            prod_stk = Stock.objects.get(seller__id=user_name.id,product__id=product.id)
            if int(price) >  0:
                if quantity < 0:
                    messages.warning(request, 'Error!! Quantity cannot be less than zero')
                else:
                    if salee.quantity > int(quantity):
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        mob_form.save()
                        temp3 = salee.quantity - int(quantity)
                        prod_stk.quantity += temp3
                        prod_stk.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_mobile_sale_product/{sid}/')
                    elif salee.quantity < int(quantity):
                        temp4 = int(quantity) - salee.quantity
                        if prod_stk.quantity > temp4:
                            sale = get_object_or_404(Sale,pk=sid)
                            sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                            sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                            sale.save()
                            sal.product = product
                            sal.save()
                            sale.total_price += (int(price) * int(quantity))
                            sale.actual_total_price += (product.price * int(quantity))
                            sale.save()
                            mob_form.save()
                            prod_stk.quantity -= temp4
                            prod_stk.save()
                            messages.success(request, 'Success!! Product details updated sucessfully')
                            return redirect(f'/view_mobile_sale_product/{sid}/')
                        else:
                            messages.warning(request, f'!!!Error!!! You can only add {prod_stk} products')
                    else:
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        mob_form.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_mobile_sale_product/{sid}/')
            else:
                messages.warning(request, f'!!!Error!!! Price has to be greater than zero')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_mobile_sale_product.html', {'sal':sal,'products':products,'mob_form':mob_form,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def edit_electronic_sale_product(request,pid):
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    sal = get_object_or_404(Product_Group,pk=pid)
    salee = get_object_or_404(Product_Group,pk=pid)
    sid = sal.sale.id
    ele_form = UpdateSaleProductForm(instance=sal)
    if request.method == 'POST':
        ele_form = UpdateSaleProductForm(request.POST,instance=sal)
        if ele_form.is_valid():
            quantity = ele_form.cleaned_data['quantity']
            price = ele_form.cleaned_data['price']
            prod = request.POST['prod']
            product = get_object_or_404(Product,pk=int(prod))
            prod_stk = Stock.objects.get(seller__id=user_name.id,product__id=product.id)
            if int(price) >  0:
                if quantity < 0:
                    messages.warning(request, 'Error!! Quantity cannot be less than zero')
                else:
                    if salee.quantity > int(quantity):
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        ele_form.save()
                        temp3 = salee.quantity - int(quantity)
                        prod_stk.quantity += temp3
                        prod_stk.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_electronics_sale_product/{sid}/')
                    elif salee.quantity < int(quantity):
                        temp4 = int(quantity) - salee.quantity
                        if prod_stk.quantity > temp4:
                            sale = get_object_or_404(Sale,pk=sid)
                            sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                            sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                            sale.save()
                            sal.product = product
                            sal.save()
                            sale.total_price += (int(price) * int(quantity))
                            sale.actual_total_price += (product.price * int(quantity))
                            sale.save()
                            ele_form.save()
                            prod_stk.quantity -= temp4
                            prod_stk.save()
                            messages.success(request, 'Success!! Product details updated sucessfully')
                            return redirect(f'/view_electronics_sale_product/{sid}/')
                        else:
                            messages.warning(request, f'!!!Error!!! You can only add {prod_stk} products')
                    else:
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        ele_form.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_electronics_sale_product/{sid}/')
            else:
                messages.warning(request, f'!!!Error!!! Price has to be greater than zero')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_electronics_sale_product.html', {'sal':sal,'products':products,'ele_form':ele_form,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def edit_accessories_sale_product(request,pid):
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    sal = get_object_or_404(Product_Group,pk=pid)
    salee = get_object_or_404(Product_Group,pk=pid)
    sid = sal.sale.id
    acc_form = UpdateSaleProductForm(instance=sal)
    if request.method == 'POST':
        acc_form = UpdateSaleProductForm(request.POST,instance=sal)
        if acc_form.is_valid():
            quantity = acc_form.cleaned_data['quantity']
            price = acc_form.cleaned_data['price']
            prod = request.POST['prod']
            product = get_object_or_404(Product,pk=int(prod))
            prod_stk = Stock.objects.get(seller__id=user_name.id,product__id=product.id)
            if int(price) >  0:
                if quantity < 0:
                    messages.warning(request, 'Error!! Quantity cannot be less than zero')
                else:
                    if salee.quantity > int(quantity):
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        acc_form.save()
                        temp3 = salee.quantity - int(quantity)
                        prod_stk.quantity += temp3
                        prod_stk.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_accessories_sale_product/{sid}/')
                    elif salee.quantity < int(quantity):
                        temp4 = int(quantity) - salee.quantity
                        if prod_stk.quantity > temp4:
                            sale = get_object_or_404(Sale,pk=sid)
                            sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                            sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                            sale.save()
                            sal.product = product
                            sal.save()
                            sale.total_price += (int(price) * int(quantity))
                            sale.actual_total_price += (product.price * int(quantity))
                            sale.save()
                            acc_form.save()
                            prod_stk.quantity -= temp4
                            prod_stk.save()
                            messages.success(request, 'Success!! Product details updated sucessfully')
                            return redirect(f'/view_accessories_sale_product/{sid}/')
                        else:
                            messages.warning(request, f'!!!Error!!! You can only add {prod_stk} products')
                    else:
                        sale = get_object_or_404(Sale,pk=sid)
                        sale.total_price = (sale.total_price)-(salee.price * salee.quantity)
                        sale.actual_total_price = (sale.actual_total_price) - (sal.product.price * salee.quantity)
                        sale.save()
                        sal.product = product
                        sal.save()
                        sale.total_price += (int(price) * int(quantity))
                        sale.actual_total_price += (product.price * int(quantity))
                        sale.save()
                        acc_form.save()
                        messages.success(request, 'Success!! Product details updated sucessfully')
                        return redirect(f'/view_accessories_sale_product/{sid}/')
            else:
                messages.warning(request, f'!!!Error!!! Price has to be greater than zero')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'sales/edit_accessories_sale_product.html', {'sal':sal,'products':products,'acc_form':acc_form,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def electronics_home(request):
    user_name = request.user.seller
    stocks = Stock.objects.filter(seller=user_name)
    return render(request, 'sales/electronics.html', {'stocks':stocks,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def view_electronics_sale_product(request,sid):
    user_name = request.user.seller
    ele_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'sales/electronics_sale_products.html', {'ele_sales_prod':ele_sales_prod,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def electronics_sale(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
        act_total_price = request.session['act_total_p']
    else:
        select_prod = {}
        total_price = 0
        act_total_price = 0
    ele_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
            if int(quantity) > 0:
                if int(quantity) <= tar_prod.quantity:
                    if int(sell_price) > 0:
                        if 'products' in request.session:
                            if product_id in request.session['products'].keys():
                                temp = request.session['products']
                                request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                                request.session['act_total_p'] -= (int(temp[product_id][0])*int(product.price))
                            val = request.session['products']
                            val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                            request.session['products'] = val
                            val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                            val3 = request.session['act_total_p'] + (int(product.price)*int(quantity))
                            request.session['total_p'] = val2
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = val3
                            act_total_price = request.session['act_total_p']
                        else:
                            request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                            select_prod = request.session['products']
                            request.session['total_p'] = int(sell_price)*int(quantity)
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = int(product.price)*int(quantity)
                            act_total_price = request.session['act_total_p']
                    else:
                        messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
                else:
                    messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                if select_prod:
                    bal = total_price - total_amount_paid
                    if int(total_amount_paid) >= 0:
                        if bal < 0:
                            messages.warning(request, f'!!!ERROR!!! The amount paid is more than the total price.')
                        else:
                            for pro in select_prod:
                                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=int(pro))
                                tar_prod.quantity = F('quantity') - int(select_prod[pro][0]) 
                                tar_prod.save()
                            sale = Sale.objects.create(seller=user_name,total_price=total_price,actual_total_price=act_total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address,date=timezone.now())
                            Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                            for prod in select_prod:
                                product = get_object_or_404(Product,pk=int(prod))
                                quantity = int(select_prod[prod][0]) 
                                amt = int(select_prod[prod][3])
                                Product_Group.objects.create(sale=sale,product=product,quantity=quantity,price=amt)
                            acc = Account.objects.all()[0]
                            acc.balance += int(total_amount_paid)
                            acc.save()
                            del request.session['products']
                            messages.success(request, 'Success!! Sale made sucessfully')
                            return redirect('/electronics_home/')
                    else:
                        messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
                else:
                        messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/electronics_sale.html', {'total_price':total_price,'select_prod': select_prod, 'products':products,'user_name':user_name,'ele_form':ele_form,'title': 'View Sales'})


# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['electronic'])
# def view_electronics_sales(request):
    user_name = request.user.seller
    ele_sales= Sale.objects.filter(seller=user_name)
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        ele_sales= Sale.objects.filter(seller= user_name,date__date__lte=end,date__date__gte=start)
        for sale in ele_sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
        sale_no = ele_sales.count()
    return render(request, 'sales/view_electronics_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'ele_sales': ele_sales, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def accessories_home(request):
    user_name = request.user.seller
    stocks = Stock.objects.filter(seller=user_name)
    return render(request, 'sales/accessories.html', {'stocks':stocks, 'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def view_accessories_sale_product(request,sid):
    user_name = request.user.seller
    acc_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'sales/accessories_sale_products.html', {'acc_sales_prod':acc_sales_prod,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def accessories_sale(request):
    if 'products' in request.session:
        select_prod = request.session['products']
        total_price = request.session['total_p']
        act_total_price = request.session['act_total_p']
    else:
        select_prod = {}
        total_price = 0
        act_total_price = 0
    acc_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirty':
            product_id = request.POST['prod']
            product = get_object_or_404(Product,pk=product_id)
            quantity = request.POST['quantity']
            sell_price = request.POST['sell_price']
            tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
            if int(quantity) > 0:
                if int(quantity) <= tar_prod.quantity:
                    if int(sell_price) > 0:
                        if 'products' in request.session:
                            if product_id in request.session['products'].keys():
                                temp = request.session['products']
                                request.session['total_p'] -= (int(temp[product_id][0])*int(temp[product_id][3]))
                                request.session['act_total_p'] -= (int(temp[product_id][0])*int(product.price))
                            val = request.session['products']
                            val[product_id] = [quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]
                            request.session['products'] = val
                            val2 = request.session['total_p'] + (int(sell_price)*int(quantity))
                            val3 = request.session['act_total_p'] + (int(product.price)*int(quantity))
                            request.session['total_p'] = val2
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = val3
                            act_total_price = request.session['act_total_p']
                        else:
                            request.session['products'] = {product_id:[quantity,product.brand,product.name,sell_price,int(sell_price)*int(quantity)]}
                            select_prod = request.session['products']
                            request.session['total_p'] = int(sell_price)*int(quantity)
                            total_price = request.session['total_p']
                            request.session['act_total_p'] = int(product.price)*int(quantity)
                            act_total_price = request.session['act_total_p']
                    else:
                        messages.warning(request, "!!!ERROR!!! Selling Price should be more than zero")
                else:
                    messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
            else:
                messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")
        elif request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                if select_prod:
                    bal = total_price - total_amount_paid
                    if int(total_amount_paid) >= 0:
                        if bal < 0:
                            messages.warning(request, f'!!!ERROR!!! The amount paid is more than the total price.')
                        else:
                            for pro in select_prod:
                                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=int(pro))
                                tar_prod.quantity = F('quantity') - int(select_prod[pro][0]) 
                                tar_prod.save()
                            sale = Sale.objects.create(seller=user_name,total_price=total_price,actual_total_price=act_total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address,date=timezone.now())
                            Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                            for prod in select_prod:
                                product = get_object_or_404(Product,pk=int(prod))
                                quantity = int(select_prod[prod][0]) 
                                amt = int(select_prod[prod][3]) 
                                Product_Group.objects.create(sale=sale,product=product,quantity=quantity,price=amt)
                            acc = Account.objects.all()[0]
                            acc.balance += int(total_amount_paid)
                            acc.save()
                            del request.session['products']
                            messages.success(request, 'Success!! Sale made sucessfully')
                            return redirect('/accessories_home/')
                    else:
                        messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
                else:
                        messages.warning(request, "!!!ERROR!!! You didnt select any product")
    return render(request, 'sales/accessories_sale.html', {'total_price':total_price,'select_prod':select_prod, 'products':products,'user_name':user_name,'acc_form':acc_form,'title': 'View Sales'})


# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['accessory'])
# def view_accessories_sales(request):
    user_name = request.user.seller
    acc_sales= Sale.objects.filter(seller= user_name)
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        acc_sales = Sale.objects.filter(seller= user_name,date__date__lte=end,date__date__gte=start)
        for sale in acc_sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
        sale_no = acc_sales.count()
    return render(request, 'sales/view_accessories_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'acc_sales':acc_sales,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def print_mobile_invoice(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.seller
    mob_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'sales/mobile_invoice.html', {'amount_paid':amount_paid,'mob_sale':mob_sale,'payment':payment,'balance':balance, 'total_price':total_price, 'user_name':user_name,'title': 'Print Invoice'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def print_electronics_invoice(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.seller
    ele_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'sales/electronics_invoice.html', {'ele_sale':ele_sale,'amount_paid':amount_paid,'payment':payment,'balance':balance, 'total_price':total_price,'user_name':user_name,'title': 'Print Invoice'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def print_accessories_invoice(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.seller
    acc_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'sales/accessories_invoice.html', {'amount_paid':amount_paid,'acc_sale':acc_sale,'payment':payment,'balance':balance, 'total_price':total_price,'user_name':user_name,'title': 'Print Invoice'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def view_electronics_payment(request,sid):
    user_name = request.user.seller
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'sales/electronic_sale_payment.html', { 'bal':bal,'sid':sid,'payments': payments,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['electronic'])
def add_electronics_payment(request,sid):
    pay_form = AddPayment()
    ele_form = SaleForm()  
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formNineteen':
            ele_form = SaleForm(request.POST)
            if ele_form.is_valid():
                name = ele_form.cleaned_data['cust_name']
                address = ele_form.cleaned_data['cust_address']
                telephone = ele_form.cleaned_data['cust_tel']
                total_amount_paid = ele_form.cleaned_data['total_amount_paid']
                quantity = ele_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_electronics_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentytwo':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/view_electronics_payment/{sid}/')
    return render(request, 'sales/electronic_add_payment.html', {'sid':sid, 'pay_form':pay_form,'products':products,'user_name':user_name,'ele_form':ele_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def view_mobile_payment(request,sid):
    user_name = request.user.seller
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'sales/mobile_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['mobile'])
def add_mobile_payment(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_mobile_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/view_mobile_payment/{sid}/')
    return render(request, 'sales/mobile_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def view_accessories_payment(request,sid):
    user_name = request.user.seller
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'sales/accessories_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['accessory'])
def add_accessories_payment(request,sid):
    pay_form = AddPayment()
    acc_form = SaleForm()
    user_name = request.user.seller
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwenty':
            acc_form = SaleForm(request.POST)
            if acc_form.is_valid():
                name = acc_form.cleaned_data['cust_name']
                address = acc_form.cleaned_data['cust_address']
                telephone = acc_form.cleaned_data['cust_tel']
                total_amount_paid = acc_form.cleaned_data['total_amount_paid']
                quantity = acc_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_accessories_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentyone':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/view_accessories_payment/{sid}/')
    return render(request, 'sales/accessories_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'acc_form':acc_form,'title': 'View Sales'})

# cashiers views
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_home(request):
    user_name = request.user.cashier
    mob_sale=0
    ele_sale=0
    acc_sale=0
    date = timezone.now().date()
    payments = Payment.objects.filter(date__date=date)
    sales = Sale.objects.all().order_by('-id')
    saless = Sale.objects.filter(date__date=date)
   
    # total_electronic = Seller.objects.filter(type='ele',user__is_active=True).count()
    # total_accessories = Seller.objects.filter(type='acc',user__is_active=True).count()
    # total_mobile = Seller.objects.filter(type='mob',user__is_active=True).count()
    # for total_mob_sale in Sale.objects.filter(seller__type='mob'):
    #     mob_sale += total_mob_sale.total_price
    # print(mob_sale)
    # for total_ele_sale in Sale.objects.filter(seller__type='ele',date__date=date):
    #     ele_sale += total_ele_sale.total_price
    # print(ele_sale)
    # for total_acc_sale in Sale.objects.filter(seller__type='acc'):
    #     acc_sale += total_acc_sale.total_price
    # print(acc_sale)
    # total_sale=0
    # for total in Sale.objects.all():
    #     total_sale+=total.total_price
    # print(total_sale)
    return render(request, 'cashier/cashier.html', {
        # 'total_accessories':total_accessories,'total_mobile':total_mobile,
        # 'total_electronic':total_electronic,
        'date':date,'user_name':user_name,'payments': payments,'saless':saless, 'sales':sales,
        'title': 'Home-Casier'})

# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['cashier'])
# def cashier_electronic_report(request):
#     products = Product.objects.filter(category='ele')
#     user_name = request.user.cashier
#     return render(request, 'cashier/electronic_report.html',{'user_name':user_name,'products':products,'title': 'Casier-Electronics-Report'})

# incomplete
# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['cashier'])
# def cashier_add_payment(request,sid):
#     pay_form = AddPayment()
#     mob_form = SaleForm()
#     user_name = request.user.cashier
#     products = Stock.objects.filter(seller__id=user_name.id)
#     if request.method == 'POST':
#         if request.POST.get("form_type") == 'formEighteen':
#             mob_form = SaleForm(request.POST)
#             if mob_form.is_valid():
#                 name = mob_form.cleaned_data['cust_name']
#                 address = mob_form.cleaned_data['cust_address']
#                 telephone = mob_form.cleaned_data['cust_tel']
#                 total_amount_paid = mob_form.cleaned_data['total_amount_paid']
#                 quantity = mob_form.cleaned_data['quantity']
#                 product_id = request.POST['prod']
#                 product = get_object_or_404(Product,pk=product_id)
#                 total_price = product.price * quantity
#                 tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
#                 bal = total_price - total_amount_paid
#                 if int(total_amount_paid) >= 0:
#                     if int(quantity) > 0:
#                         if quantity <= tar_prod.quantity:
#                             if bal < 0:
#                                 messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
#                             else:
#                                 tar_prod.quantity = F('quantity') - quantity
#                                 tar_prod.save()
#                                 sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
#                                 Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
#                                 acc = Account.objects.all()[0]
#                                 acc.balance += int(total_amount_paid)
#                                 acc.save()
#                                 messages.success(request, 'Success!! Sale made sucessfully')
#                                 return redirect('/cashier_mobile_sales/')
#                         else:
#                             messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
#                     else:
#                         messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
#                 else:
#                     messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
#         elif request.POST.get("form_type") == 'formTwentythree':
#             pay_form = AddPayment(request.POST)
#             if pay_form.is_valid():
#                 amount = pay_form.cleaned_data['amount']
#                 descp = request.POST['desc']
#                 sale = get_object_or_404(Sale,pk=sid)
#                 total_amt = sale.total_amount_paid + amount
#                 bal = sale.total_price - total_amt
#                 val = sale.total_price - sale.total_amount_paid
#                 if amount>val:
#                     messages.warning(request, 'Error!! Amount paid more than balance')
#                 else:
#                     if descp:
#                         Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
#                     else:
#                         Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
#                     sale.total_amount_paid += amount
#                     sale.save()
#                     acc = Account.objects.all()[0]
#                     acc.balance += amount
#                     acc.save()
#                     messages.success(request, 'Success!! Payment made sucessfully')
#                     return redirect(f'/cashier_sale_payments/{sid}/')
#     return render(request, 'cashier/cashier_add_mobile_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})







@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_electronic_sales(request):
    sales = Sale.objects.all().filter(seller__type='ele')
    user_name = request.user.cashier
    val_set = ''
    total_amount = 0
    total_price = 0
    total_profit = 0
    sale_no = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        sales = Sale.objects.filter(seller__type='ele',date__date__lte=end,date__date__gte=start)
        for sale in sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
            total_profit += (sale.total_price - sale.actual_total_price)
        sale_no = sales.count()
    return render(request, 'cashier/electronic_sales.html', {'total_profit':total_profit,'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'user_name':user_name,'sales': sales,'title': 'Casier-Electronics-Sales'})

# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['cashier'])
# def cashier_accessories_report(request):
#     products = Product.objects.filter(category='acc')
#     user_name = request.user.cashier
#     return render(request, 'cashier/accessories_report.html', {'user_name':user_name,'products': products,'title': 'Casier-Accessories-Report'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_mobile_sellers(request):
    sellers = Seller.objects.filter(type='mob',user__is_active=True)
    user_name = request.user.cashier
    return render(request, 'cashier/mobile_sellers.html',{'user_name':user_name,'sellers':sellers, 'title':'Cashier-Mobile-Sellers'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_electronic_sellers(request):
    sellers = Seller.objects.filter(type='ele',user__is_active=True)
    user_name = request.user.cashier
    return render(request, 'cashier/electronic_sellers.html',{'user_name':user_name,'sellers':sellers, 'title':'Cashier-Mobile-Sellers'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_accessories_sellers(request):
    sellers = Seller.objects.filter(type='acc',user__is_active=True)
    user_name = request.user.cashier
    return render(request, 'cashier/accessories_sellers.html',{'user_name':user_name,'sellers':sellers, 'title':'Cashier-Mobile-Sellers'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_accessories_sales(request):
    sales = Sale.objects.all().filter(seller__type='acc')
    user_name = request.user.cashier
    val_set = ''
    total_amount = 0
    total_price = 0
    total_profit = 0
    sale_no = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        sales = Sale.objects.filter(seller__type='acc',date__date__lte=end,date__date__gte=start)
        for sale in sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
            total_profit += (sale.total_price - sale.actual_total_price)
        sale_no = sales.count()
    return render(request, 'cashier/accessories_sales.html', {'total_profit':total_profit,'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'user_name':user_name,'sales': sales,'title': 'Casier-Accessories-Sales'})

# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['cashier'])
# def cashier_mobile_report(request):
#     products = Product.objects.filter(category='mob')
#     user_name = request.user.cashier
#     return render(request, 'cashier/mobile_report.html', {'user_name':user_name,'products': products,'title': 'Casier-Mobile-Report'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_sale_payments(request,sid):
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    user_name = request.user.cashier
    total_payments = 0
    for payment in payments:
        total_payments += payment.amount
    bal = sale.total_price - total_payments
    return render(request, 'cashier/sale_payments.html', {'bal':bal,'user_name':user_name,'payments': payments,'title': 'Casier-Sales'})

# mobile
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_view_mobile_payment(request,sid):
    user_name = request.user.cashier
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'cashier/cashier_mobile_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_add_mobile_payment(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.cashier
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_mobile_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/cashier_view_mobile_payment/{sid}/')
    return render(request, 'cashier/cashier_mobile_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

# accessory
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_view_accessory_payment(request,sid):
    user_name = request.user.cashier
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'cashier/cashier_accessory_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_add_accessory_payment(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.cashier
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_mobile_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/cashier_view_accessory_payment/{sid}/')
    return render(request, 'cashier/cashier_accessory_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

# Electronic
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_view_electronic_payment(request,sid):
    user_name = request.user.cashier
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'cashier/cashier_electronic_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['cashier'])
# def cashier_add_electronic_payment(request,sid):
#     pay_form = AddPayment()
#     mob_form = SaleForm()
#     user_name = request.user.cashier
#     products = Stock.objects.filter(seller__id=user_name.id)
#     if request.method == 'POST':
#         if request.POST.get("form_type") == 'formEighteen':
#             mob_form = SaleForm(request.POST)
#             if mob_form.is_valid():
#                 name = mob_form.cleaned_data['cust_name']
#                 address = mob_form.cleaned_data['cust_address']
#                 telephone = mob_form.cleaned_data['cust_tel']
#                 total_amount_paid = mob_form.cleaned_data['total_amount_paid']
#                 quantity = mob_form.cleaned_data['quantity']
#                 product_id = request.POST['prod']
#                 product = get_object_or_404(Product,pk=product_id)
#                 total_price = product.price * quantity
#                 tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
#                 bal = total_price - total_amount_paid
#                 if int(total_amount_paid) >= 0:
#                     if int(quantity) > 0:
#                         if quantity <= tar_prod.quantity:
#                             if bal < 0:
#                                 messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
#                             else:
#                                 tar_prod.quantity = F('quantity') - quantity
#                                 tar_prod.save()
#                                 sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
#                                 Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
#                                 acc = Account.objects.all()[0]
#                                 acc.balance += int(total_amount_paid)
#                                 acc.save()
#                                 messages.success(request, 'Success!! Sale made sucessfully')
#                                 return redirect('/view_mobile_sales/')
#                         else:
#                             messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
#                     else:
#                         messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
#                 else:
#                     messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
#         elif request.POST.get("form_type") == 'formTwentythree':
#             pay_form = AddPayment(request.POST)
#             if pay_form.is_valid():
#                 amount = pay_form.cleaned_data['amount']
#                 descp = request.POST['desc']
#                 sale = get_object_or_404(Sale,pk=sid)
#                 total_amt = sale.total_amount_paid + amount
#                 bal = sale.total_price - total_amt
#                 val = sale.total_price - sale.total_amount_paid
#                 if amount>val:
#                     messages.warning(request, 'Error!! Amount paid more than balance')
#                 else:
#                     if descp:
#                         Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
#                     else:
#                         Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
#                     sale.total_amount_paid += amount
#                     sale.save()
#                     acc = Account.objects.all()[0]
#                     acc.balance += amount
#                     acc.save()
#                     messages.success(request, 'Success!! Payment made sucessfully')
#                     return redirect(f'/cashier_view_electronic_payment/{sid}/')
#     return render(request, 'cashier/cashier_electronic_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_sale_products(request,sid):
    user_name = request.user.cashier
    sales_prod = Product_Group.objects.filter(sale__id=sid)
    
    return render(request, 'cashier/sale_products.html', {'user_name':user_name,'sales_prod': sales_prod,'title': 'Casier-Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_sale_view(request,sid):
    user_name = request.user.cashier
    sales_prod = Product_Group.objects.filter(sale__id=sid)
    view = Sale.objects.get(id=sid)
    view.view_counts += 1
    view.save()
    return render(request, 'cashier/cashier_sale_view.html', {'user_name':user_name,'sales_prod': sales_prod,'title': 'Casier-Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_new_exp(request):
    user_name = request.user.cash
    exp_form = CashExpenditureForm()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyFive':
            exp_form = CashExpenditureForm(request.POST)
            if exp_form.is_valid():

                reciepient = exp_form.cleaned_data['reciepient'] 
                category = exp_form.cleaned_data['category']
                desc = exp_form.cleaned_data['desc'] 
                amount = exp_form.cleaned_data['amount']
                if int(amount)<0:
                    messages.warning(request, "!!!ERROR!!! Amount has to be greater than zero")
                else:
                    CashExpense.objects.create(category=category,reciepient=reciepient,desc=desc,amount=amount,date=timezone.now())
                    acc = CashAccount.objects.all()[0]
                    acc.balance -= int(amount)
                    acc.save()
                    messages.success(request, 'Success!! New Expenditure added sucessfully')
                    return redirect('/cash_other_expenses/') 
    return render(request, 'cash/cash_new_exp.html',{'exp_form':exp_form,'user_name':user_name,})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_new_exp_type(request):
    user_name = request.user.cash
    exp_type_form = ExpenditureTypeForm()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyFive':
            exp_type_form = ExpenditureTypeForm(request.POST)
            if exp_type_form.is_valid():
                title = exp_type_form.cleaned_data['title'] 
               
                ExpenseType.objects.create(title=title,date=timezone.now())
                    
                messages.success(request, 'Success!! New Expenditure Type added sucessfully')
                return redirect('/cash_expenditure_type/') 
    return render(request, 'cash/cash_new_exp_type.html',{'exp_type_form':exp_type_form,'user_name':user_name,})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_expenditure_type(request):
    user_name = request.user.cash
    expenses = ExpenseType.objects.all()
    return render(request, 'cash/cash_expenditure_type.html',{'expenses':expenses,'user_name':user_name})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_other_exp(request):
    expenses = CashExpense.objects.all()
    user_name = request.user.cash
    val_set = ''
    total_amount = 0
    total_exp = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Expenitures from {start} to {end}'
        expenses = CashExpense.objects.filter(date__date__lte=end,date__date__gte=start)
        for exp in expenses:
            total_exp += 1
            total_amount += exp.amount
    return render(request, 'cash/other_expenditure.html',{'total_exp':total_exp,'val_set':val_set,'total_amount':total_amount,'expenses':expenses,'user_name':user_name})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def cashier_mobile_sales(request):
    sales = Sale.objects.all().filter(seller__type='mob')
    user_name = request.user.cashier
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    total_profit = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        sales = Sale.objects.filter(seller__type='mob',date__date__lte=end,date__date__gte=start)
        for sale in sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
            total_profit += (sale.total_price - sale.actual_total_price)
        sale_no = sales.count()
    return render(request, 'cashier/mobile_sales.html', {'total_profit':total_profit,'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'user_name':user_name,'sales': sales,'title': 'Casier-Mobile-Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cashier'])
def print_cashier_invoice(request,pid):
    user_name = request.user.cashier
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    amount_paid = payment.total_amount
    sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'cashier/invoice.html',{'balance':balance, 'amount_paid':amount_paid,'sale':sale,'user_name':user_name,'total_price': total_price,'sale':sale,'payment':payment})

def sum_price(a,b):
    return a*b

def total_balance(a,b):
    return a-b
#mobile

# cash
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_home(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    bor_form = BorrowerForm()
    sales = RecordedSale.objects.all()
    total_balance= 0
    total_exp= 0
    total_sales = 0
    total_deposit = 0
    total_borrow =0
    total_savings = 0
    for saving in Saving.objects.all():
        total_savings += saving.amount
    for borrow in CashBorrower.objects.all():
        total_borrow += borrow.balance
    for deposit in CashDepositor.objects.all():
        total_deposit += deposit.balance
    for sale in RecordedSale.objects.all():
        total_sales += sale.amount
    for expenses in CashExpenses.objects.all():
        total_exp += expenses.balance
    balance = CashAccount.objects.all()
    for bal in balance:
        total_balance += bal.balance
    amount = 0
    val_set = ''
    
    if request.method == 'POST': 
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        sales = RecordedSale.objects.filter(date__date__lte=end,date__date__gte=start)
        for sale in sales:
            amount += sale.amount
    sale_no=sales.count()    
    return render(request,'cash/cash.html' ,{'total_savings':total_savings, "total_borrow":total_borrow, 'total_deposit':total_deposit, 'total_sales':total_sales, 'total_exp':total_exp, 'total_balance':total_balance, 'sale_no':sale_no, 'val_set':val_set, 'amount':amount, 'sales':sales, 'dep_form':dep_form,'stk':stk,'bor_form':bor_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_add_savings(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    bor_form = CashBorrowerForm()
    user_name = request.user.cash
    add_savings = SavingForm()
    if request.method == 'POST':
        add_savings = SavingForm(request.POST, request.FILES)
        if add_savings.is_valid():
            bank = add_savings.cleaned_data['bank']
            amount = add_savings.cleaned_data['amount']
            description = add_savings.cleaned_data['description']
            image = add_savings.cleaned_data['image']
            Saving.objects.create(bank=bank,amount=amount,description=description, image=image)
            messages.success(request,"Savings added successfully")
            return redirect('/cash_view_savings/')
    
        
    return render(request,'cash/cash_add_savings.html',{'user_name':user_name,'add_savings':add_savings,'dep_form':dep_form, 'bor_form':bor_form })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_view_savings(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    bor_form = CashBorrowerForm()
    user_name= request.user.cash
    savings = Saving.objects.all()
    return render(request, 'cash/cash_view_savings.html',{'dep_form':dep_form, 'bor_form':bor_form, 'stk':stk, 'user_name':user_name, 'savings':savings,})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_cashexp(request,eid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    exp = get_object_or_404(CashExpense,pk=eid)
    exp_form = CashExpenditureForm(instance=exp)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyFive':
            exp_form = CashExpenditureForm(request.POST)
            if exp_form.is_valid():
                category = exp_form.cleaned_data['category']
                reciepient = exp_form.cleaned_data['reciepient'] 
                desc = exp_form.cleaned_data['desc'] 
                amount = exp_form.cleaned_data['amount']
                if int(amount)<0:
                    messages.warning(request, "!!!ERROR!!! Amount has to be greater than zero")
                else:
                    amt = exp.amount
                    acc = Account.objects.all()[0]
                    acc.balance += int(amt)
                    exp.category = category 
                    exp.reciepient = reciepient
                    exp.desc = desc
                    exp.amount = amount
                    exp.save()
                    acc.balance -= int(amount)
                    acc.save()
                    messages.success(request, 'Success!! Expenditure updated sucessfully')
                    return redirect('/cash_other_expenses/') 
    return render(request, 'cash/cash_edit_exp.html',{'exp_form':exp_form,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_view_depositors(request):
    depositor_list = CashDepositor.objects.all()
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            dep_form = CashDepositorForm(request.POST)
            if dep_form.is_valid():
                amt = dep_form.cleaned_data['balance']
                acc = CashAccount.objects.all()[0]
                acc.balance += int(amt)
                acc.save()
                dep = dep_form.save()
                CashTransaction.objects.create(depositor=dep,action='Deposit',amount=amt,date=timezone.now())
                messages.success(request, 'Success!! Depositor created sucessfully')
                return redirect('/cash_view_depositors/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'cash/cash_view_depositors.html', {'user_name':user_name,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_view_borrowers(request):
    borrower_list = CashBorrower.objects.all()
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    acc = CashAccount.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
            bor_form = CashBorrowerForm(request.POST)
            if bor_form.is_valid():
                amt = bor_form.cleaned_data['balance']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = bor_form.save()
                    CashBorrower_Transaction.objects.create(borrower=dep,action='Borrower',amount=amt,date=timezone.now())
                    messages.success(request, 'Success!! Borrower created sucessfully')
                    return redirect('/cash_view_borrowers/')
                else:
                    messages.warning(request, 'Error!! Borrow cannot be More than the balance')
                    return redirect('/cash_view_borrowers/')
            else:
                messages.warning(request, 'Error!! Borrower cannot Borrow more than the company balance')
            return redirect('/cash_view_borrowers/')
           
    return render(request, 'cash/cash_view_borrowers.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'borrower_list': borrower_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_borrower_transactions(request,bor_pk):
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    bor_trans = CashBorrower_Transaction.objects.filter(borrower_id=bor_pk)
    bor = get_object_or_404(CashBorrower,pk=bor_pk)
    borname = bor.fname + ' ' + bor.lname
    val_set = ''
    total_amt = 0
    total_rep = 0
    total_bor = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transaction for {borname} from {start} to {end}'
        bor_trans = CashBorrower_Transaction.objects.filter(borrower_id=bor_pk,date__date__lte=end,date__date__gte=start)
        for trans in bor_trans:
            total_amt += 1
            if trans.action == 'Borrow':
                total_bor += trans.amount
            elif trans.action == 'Repay':
                total_rep += trans.amount

    return render(request, 'cash/cash_borrower_transactions.html', { 'val_set':val_set,'total_amt':total_amt,'total_rep':total_rep,'total_bor':total_bor,'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'bor_trans': bor_trans,'bor': bor, 'borname':borname})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_view_expenses(request):
    expenses_list = CashExpenses.objects.all()
    stk = Stock.objects.filter(quantity=0)
    expenses_form = CashExpensesForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    acc = CashAccount.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
            expenses_form = CashExpensesForm(request.POST)
            if expenses_form.is_valid():
                amt = expenses_form.cleaned_data['balance']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = expenses_form.save()
                    CashExpenses_Transaction.objects.create(expense=dep,action='Expense',amount=amt,date=timezone.now())
                    messages.success(request, 'Success!! Expense created sucessfully')
                    return redirect('/cash_view_expenses/')
                else:
                    messages.warning(request, 'Error!! Expense cannot be More than the balance')
                    return redirect('/cash_view_expenses/')
            else:
                messages.warning(request, 'Error!! Expenditure cannot be more than the company balance')
            return redirect('/cash_view_expenses/')
           
    return render(request, 'cash/cash_view_expenses.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'expenses_form':expenses_form,'expenses_list': expenses_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_expenses_transactions(request,exp_pk):
    stk = Stock.objects.filter(quantity=0)
    expenses_form = CashExpensesForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    expenses_trans = CashExpenses_Transaction.objects.filter(expense_id=exp_pk)
    exp = get_object_or_404(CashExpenses,pk=exp_pk)
    carname = exp.category 
    val_set = ''
    total_amt = 0
    total_rep = 0
    total_bor = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transaction for {carname} from {start} to {end}'
        expenses_trans = CashExpenses_Transaction.objects.filter(expense_id=exp,date__date__lte=end,date__date__gte=start)
        for trans in expenses_trans:
            total_amt += 1
            if trans.action == 'Expense':
                total_bor += trans.amount
            elif trans.action == 'Payment':
                total_rep += trans.amount

    return render(request, 'cash/cash_expenses_transactions.html', { 'val_set':val_set,'total_amt':total_amt,'total_rep':total_rep,'total_bor':total_bor,'user_name':user_name,'stk':stk,'prod_form':prod_form,'expenses_form':expenses_form,'expenses_trans': expenses_trans,'exp': exp, 'carname':carname})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def expenses_transactions(request,exp_pk):
    stk = Stock.objects.filter(quantity=0)
    expenses_form = ExpensesForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    expenses_trans = Expense_Transaction.objects.filter(expense_id=exp_pk)
    exp = get_object_or_404(Expense,pk=exp_pk)
    carname = exp.category 
    val_set = ''
    total_amt = 0
    total_rep = 0
    total_bor = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transaction for {carname} from {start} to {end}'
        expenses_trans = Expense_Transaction.objects.filter(expense_id=exp,date__date__lte=end,date__date__gte=start)
        for trans in expenses_trans:
            total_amt += 1
            if trans.action == 'Expense':
                total_bor += trans.amount
            elif trans.action == 'Payment':
                total_rep += trans.amount

    return render(request, 'admin/expenses_transactions.html', { 'val_set':val_set,'total_amt':total_amt,'total_rep':total_rep,'total_bor':total_bor,'user_name':user_name,'stk':stk,'prod_form':prod_form,'expenses_form':expenses_form,'expenses_trans': expenses_trans,'exp': exp, 'carname':carname})




@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_depositor_transactions(request,dep_pk):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    dep_trans = CashTransaction.objects.filter(depositor_id=dep_pk)
    dep = get_object_or_404(CashDepositor,pk=dep_pk)
    depname = dep.fname + ' ' + dep.lname
    val_set = ''
    total_amt = 0
    total_dep = 0
    total_wit = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transactions for {depname} from {start} to {end}'
        dep_trans = CashTransaction.objects.filter(depositor_id=dep_pk,date__date__lte=end,date__date__gte=start)
        for trans in dep_trans:
            total_amt += 1
            if trans.action == 'Withdraw':
                total_wit += trans.amount
            elif trans.action == 'Deposit':
                total_dep += trans.amount
    return render(request, 'cash/cash_depositor_transactions.html', {'val_set':val_set,'total_amt':total_amt,'total_dep':total_dep,'total_wit':total_wit,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'dep_trans': dep_trans,'dep': dep})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_depositor_deposit(request,did):
    des_form = CashDepositForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeven':
                des_form = CashDepositForm(request.POST)
                if des_form.is_valid():
                    amount = des_form.cleaned_data['amount']
                    description = des_form.cleaned_data['description']
                    dep = get_object_or_404(CashDepositor,pk=did)
                    dep.balance = F('balance') + amount
                    dep.save()
                    trans = CashTransaction.objects.create(depositor=dep,action='Deposit',amount=amount,description=description,  date=timezone.now())
                    acc = CashAccount.objects.all()[0]
                    acc.balance += int(amount)
                    acc.save()
                    messages.success(request, 'Success!! Transaction completed sucessfully')
                    return redirect(f'/cash_depositor_transactions/{did}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_depositor_deposit.html', {'user_name':user_name,'did':did,'stk':stk,'des_form':des_form,'prod_form':prod_form,'dep_form':dep_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_depositor_withdraw(request,did):
    wit_form = CashWithdrawForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEight':
                wit_form = CashWithdrawForm(request.POST)
                if wit_form.is_valid():
                    amount = wit_form.cleaned_data['amount']
                    description = wit_form.cleaned_data['description']
                    dep = get_object_or_404(CashDepositor,pk=did)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = CashTransaction.objects.create(depositor=dep,action='Withdraw',amount=amount ,description=description,date=timezone.now())
                        acc = CashAccount.objects.all()[0]
                        acc.balance -= int(amount)
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                        return redirect(f'/cash_depositor_transactions/{did}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Insufficient Funds!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")
                    return redirect(f'/cash_depositor_transactions/{did}/')
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_depositor_withdraw.html', {'user_name':user_name,'did':did,'stk':stk,'wit_form':wit_form,'prod_form':prod_form,'dep_form':dep_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_depositor(request,did):
    dep = get_object_or_404(CashDepositor,pk=did)
    up_dep = UpdateCashDepositorForm(instance=dep)
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            up_dep = UpdateCashDepositorForm(request.POST,instance=dep)
            if up_dep.is_valid():
                up_dep.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/cash_view_depositors/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    depositor_list = CashDepositor.objects.all()
    return render(request, 'cash/cash_edit_depositor.html', {'user_name':user_name,'stk':stk,'up_dep':up_dep,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_saving(request,sid):
    save = get_object_or_404(Saving,pk=sid)
    up_saving = UpdateSavingForm(instance=save)
    user_name = request.user.cash
    if request.method == 'POST':
            up_saving = UpdateSavingForm(request.POST, request.FILES,instance=save)
            if up_saving.is_valid():
                up_saving.save()
                messages.success(request, 'Success!! Saving updated sucessfully')
                return redirect(f'/cash_view_savings/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    product_list = Saving.objects.all()
    return render(request, 'cash/cash_edit_saving.html', {'user_name':user_name,'up_saving':up_saving,'product_list': product_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_sale(request,sid):
    save = get_object_or_404(RecordedSale,pk=sid)
    up_saving = UpdateRecordedSaleForm(instance=save)
    user_name = request.user.cash
    if request.method == 'POST':
            up_saving = UpdateRecordedSaleForm(request.POST, request.FILES,instance=save)
            if up_saving.is_valid():
                up_saving.save()
                messages.success(request, 'Success!! SALE updated sucessfully')
                return redirect(f'/cash_view_recorded_sales/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    product_list = Saving.objects.all()
    return render(request, 'cash/cash_edit_sale.html', {'user_name':user_name,'up_saving':up_saving,'product_list': product_list})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_borrower(request,bid):
    bor = get_object_or_404(CashBorrower,pk=bid)
    up_bor = UpdateCashBorrowerForm(instance=bor)
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFourtty':
            up_bor = UpdateCashBorrowerForm(request.POST,instance=bor)
            if up_bor.is_valid():
                up_bor.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/cash_view_borrowers/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    borrower_list = CashBorrower.objects.all()
    return render(request, 'cash/cash_edit_borrower.html', {'user_name':user_name,'stk':stk,'up_bor':up_bor,'prod_form':prod_form,'bor_form':bor_form,'borrower_list': borrower_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_edit_expenses(request,eid):
    exp = get_object_or_404(CashExpenses,pk=eid)
    exp_up = UpdateCashExpensesForm(instance=exp)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFifty':
            exp_up = UpdateCashExpensesForm(request.POST,instance=exp)
            if exp_up.is_valid():
                exp_up.save()
                messages.success(request, 'Success!! Expense updated sucessfully')
                return redirect('/cash_view_expenses/')
            else:
                messages.warning(request,'!!!ERRORrrrr!!! Try Again')
    expenses_list = CashExpenses.objects.all()
    return render(request, 'cash/cash_edit_expenses.html', {'user_name':user_name,'stk':stk,'exp_up':exp_up,'prod_form':prod_form,'exp_form':exp_form,'expenses_list': expenses_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_expenses(request,eid):
    exp = get_object_or_404(Expense,pk=eid)
    exp_up = UpdateExpensesForm(instance=exp)
    stk = Stock.objects.filter(quantity=0)
    exp_form = ExpensesForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFifty':
            exp_up = UpdateExpensesForm(request.POST,instance=exp)
            if exp_up.is_valid():
                exp_up.save()
                messages.success(request, 'Success!! Expense updated sucessfully')
                return redirect('/admin_view_shop_expenses/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    expenses_list = Expense.objects.all()
    return render(request, 'admin/edit_expenses.html', {'user_name':user_name,'stk':stk,'exp_up':exp_up,'prod_form':prod_form,'exp_form':exp_form,'expenses_list': expenses_list})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_borrower_repay(request,bid):
    rep_form = CashRepayForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeventy':
                rep_form = CashRepayForm(request.POST)
                if rep_form.is_valid():
                    amount = rep_form.cleaned_data['amount']
                    description=rep_form.cleaned_data['description']
                    dep = get_object_or_404(CashBorrower,pk=bid)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = CashBorrower_Transaction.objects.create(borrower=dep,action='Repay',amount=amount, description=description, date=timezone.now())
                        acc = CashAccount.objects.all()[0]
                        acc.balance += int(amount)  
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                    else:
                         messages.warning(request, '!!!Error!!! Transaction Fail!! Amount Cant be greater than Balance')
                    return redirect(f'/cash_borrower_transactions/{bid}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_borrower_repay.html', { 'user_name':user_name,'bid':bid,'stk':stk,'rep_form':rep_form,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_borrower_borrowed(request,bid):
    wit_form = CashBorrowForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    acc = CashAccount.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
                wit_form = CashBorrowForm(request.POST)
                if wit_form.is_valid():
                    amount = wit_form.cleaned_data['amount']
                    description = wit_form.cleaned_data['description']
                    dep = get_object_or_404(CashBorrower,pk=bid)
                    if amount >= 0:
                        if amount <= acc.balance:
                            dep.balance = F('balance') + amount
                            dep.save()
                            trans = CashBorrower_Transaction.objects.create(borrower=dep,action='Borrow',amount=amount, description=description,date=timezone.now())
                        
                        
                            acc.balance -= int(amount)
                            acc.save()
                            messages.success(request, 'Success!! Transaction completed sucessfully')
                        else:
                             messages.warning(request, 'Error!! Transaction Fail, Amount Cant be Greater than Company balance')
                        return redirect(f'/cash_borrower_transactions/{bid}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed Amount Can't be less than Zero")
                    return redirect(f'/cash_borrower_transactions/{bid}/')
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_borrower_borrowed.html', {'user_name':user_name,'bid':bid,'stk':stk,'bor_form':bor_form,'prod_form':prod_form,'wit_form':wit_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_expenses_repay(request,eid):
    rep_form = CashExpensesRepayForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeventy':
                rep_form = CashExpensesRepayForm(request.POST)
                if rep_form.is_valid():
                    amount = rep_form.cleaned_data['amount']
                    description=rep_form.cleaned_data['description']
                    dep = get_object_or_404(CashExpenses,pk=eid)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = CashExpenses_Transaction.objects.create(expense=dep,action='Payment',amount=amount, description=description, date=timezone.now())
                        acc = CashAccount.objects.all()[0]
                        acc.balance += int(amount)  
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                    else:
                         messages.warning(request, '!!!Error!!! Transaction Fail!! Amount Cant be greater than Balance')
                    return redirect(f'/cash_expenses_transactions/{eid}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_expenses_repay.html', { 'user_name':user_name,'eid':eid,'stk':stk,'rep_form':rep_form,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def expenses_repay(request,eid):
    rep_form = ExpensesRepayForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeventy':
                rep_form = ExpensesRepayForm(request.POST)
                if rep_form.is_valid():
                    amount = rep_form.cleaned_data['amount']
                    description=rep_form.cleaned_data['description']
                    dep = get_object_or_404(Expense,pk=eid)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = Expense_Transaction.objects.create(expense=dep,action='Payment',amount=amount, description=description, date=timezone.now())
                        acc = Account.objects.all()[0]
                        acc.balance += int(amount)  
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                    else:
                         messages.warning(request, '!!!Error!!! Transaction Fail!! Amount Cant be greater than Balance')
                    return redirect(f'/expenses_transactions/{eid}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'admin/expenses_repay.html', { 'user_name':user_name,'eid':eid,'stk':stk,'rep_form':rep_form,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_add_expenses(request,eid):
    exp_form = CashExpenseForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = CashBorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.cash
    acc = CashAccount.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
                exp_form = CashExpenseForm(request.POST)
                if exp_form.is_valid():
                    amount = exp_form.cleaned_data['amount']
                    description = exp_form.cleaned_data['description']
                    dep = get_object_or_404(CashExpenses,pk=eid)
                    if amount >= 0:
                        if amount <= acc.balance:
                            dep.balance = F('balance') + amount
                            dep.save()
                            trans = CashExpenses_Transaction.objects.create(expense=dep,action='Expense',amount=amount, description=description,date=timezone.now())
                        
                        
                            acc.balance -= int(amount)
                            acc.save()
                            messages.success(request, 'Success!! Transaction completed sucessfully')
                        else:
                             messages.warning(request, 'Error!! Transaction Fail, Amount Cant be Greater than Company balance')
                        return redirect(f'/cash_expenses_transactions/{eid}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed Amount Can't be less than Zero")
                    return redirect(f'/cash_expenses_transactions/{eid}/')
    sales_list = Sale.objects.all()
    return render(request, 'cash/cash_expenses_expense.html', {'user_name':user_name,'eid':eid,'stk':stk,'bor_form':bor_form,'prod_form':prod_form,'exp_form':exp_form,'sales_list': sales_list})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def add_expenses(request,eid):
    exp_form = ExpensesForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
                exp_form = ExpensesForm(request.POST)
                if exp_form.is_valid():
                    amount = exp_form.cleaned_data['amount']
                    description = exp_form.cleaned_data['description']
                    dep = get_object_or_404(Expense,pk=eid)
                    if amount >= 0:
                        if amount <= acc.balance:
                            dep.balance = F('balance') + amount
                            dep.save()
                            trans = Expense_Transaction.objects.create(expense=dep,action='Expense',amount=amount, description=description,date=timezone.now())
                        
                            acc.balance -= int(amount)
                            acc.save()
                            messages.success(request, 'Success!! Transaction completed sucessfully')
                        else:
                             messages.warning(request, 'Error!! Transaction Fail, Amount Cant be Greater than Company balance')
                        return redirect(f'/expenses_transactions/{eid}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed Amount Can't be less than Zero")
                    return redirect(f'/expenses_transactions/{eid}/')
    sales_list = Sale.objects.all()
    return render(request, 'admin/expenses_expense.html', {'user_name':user_name,'eid':eid,'stk':stk,'bor_form':bor_form,'prod_form':prod_form,'exp_form':exp_form,'sales_list': sales_list})




@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_record_sale(request):
    user_name = request.user.cash
    if request.method == 'POST':
        add_record = RecordedSaleForm(request.POST)
        if add_record.is_valid():
            amount = add_record.cleaned_data['amount']
            acc = CashAccount.objects.all()[0]
            acc.balance += int(amount)
            acc.save()
            RecordedSale.objects.create(cash=user_name,amount=amount)
            messages.success(request, 'Success!! Sale recorded sucessfully')
            return redirect('/cash_view_recorded_sales/')
    else:
        add_record=RecordedSaleForm()
        
   
    return render(request, 'cash/cash_record_sale.html', {'user_name':user_name, 'add_record':add_record})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['cash'])
def cash_view_recorded_sales(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = CashDepositorForm()
    bor_form = CashBorrowerForm()
    user_name= request.user.cash
    recordedsales = RecordedSale.objects.all()
    return render(request, 'cash/cash_view_recorded_sales.html',{'dep_form':dep_form, 'bor_form':bor_form, 'stk':stk, 'user_name':user_name, 'recordedsales':recordedsales,})



# admin views
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_home(request):  
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    total_users = User.objects.filter(is_active=True,is_admin=False).count()
    total_electronic = Seller.objects.filter(type='ele',user__is_active=True).count()
    total_accessories = Seller.objects.filter(type='acc',user__is_active=True).count()
    total_mobile = Seller.objects.filter(type='mob',user__is_active=True).count()
    total_aux = Staff.objects.all().count()
    total_admins = Sup_user.objects.filter(user__is_active=True).count()
    total_cashiers = Cashier.objects.filter(user__is_active=True).count()
    top_mob = Sale.objects.filter(seller__type='mob').order_by('-total_price')[:5]
    top_ele = Sale.objects.filter(seller__type='ele').order_by('-total_price')[:5]
    top_acc = Sale.objects.filter(seller__type='acc').order_by('-total_price')[:5]
    total_exp = 0
    total_sales = 0
    num_today_sale = 0
    total_today_sale=0
    today_total_profit=0
    total_amount_today=0
    today_cre_bal=0
    for exp in Expense.objects.all():
        total_exp += exp.balance
    for sal in Salaries.objects.all():
        total_exp += sal.amount
    top_dep = Depositor.objects.all().order_by('-balance')[:5]
    total_balance = Account.objects.all()[0].balance
    date = timezone.now().date()
    today_sales = Sale.objects.filter(date__date=date)
    # today_payments = Payment.objects.filter(date__date=date)
    num_today_cred=0
    amount_deposit = 0
    add_deposit = 0
    add_borrower=0
    all_total_amount_today=0
       
    for tsale in Sale.objects.filter(date__date=date):
        total_today_sale += tsale.total_price
        total_amount_today += tsale.total_amount_paid
        num_today_sale +=1
        today_total_profit+= (tsale.total_price - tsale.actual_total_price)
        if tsale.total_amount_paid < tsale.total_price:
            today_cre_bal += tsale.total_price - tsale.total_amount_paid
            num_today_cred+=1
    for dep1 in Transaction.objects.all():
        if dep1.action == 'Deposit':
            add_deposit += dep1.amount
        else:
            add_deposit -= dep1.amount
    moneyin=0
    total_sale_amount =0
    exps_amount = 0
    add_borrower1 = 0
    add_depositor1 = 0
    for sale in Sale.objects.all():
        total_sale_amount += sale.total_amount_paid
    for exps in Expense.objects.all():
        exps_amount += exps.balance
    for bor1 in Borrower_Transaction.objects.all():
        if bor1.action == 'Borrow':
            add_borrower += bor1.amount
        else:
            add_borrower -= bor1.amount
    for bor1 in Borrower.objects.all():
        
        add_borrower1 += bor1.balance
    for dep1 in Depositor.objects.all():
        
        add_depositor1 += dep1.balance
     
    all_total_amount_today = (total_sale_amount + add_depositor1) - (add_borrower1 + exps_amount) 
    
    mob_amount = 0
    ele_amount = 0
    acc_amount = 0
    cre_amount = 0
    actual_total_sales=0
    cre_bal = 0
    dep_bal = 0
    t_mob=0
    t_ele=0
    t_acc=0
    
    dep_amount = 0
    bor_amount=0
    bor_bal=0
    for prod in Product.objects.all():
        if prod.category=='mob':
            mob_amount += prod.total_quantity
            t_mob += prod.price*prod.total_quantity
        elif prod.category=='ele':
            ele_amount += prod.total_quantity
            t_ele += prod.price*prod.total_quantity
        elif prod.category=='acc':
            acc_amount += prod.total_quantity
            t_acc += prod.price*prod.total_quantity
    for sale in Sale.objects.all():
        if sale.total_amount_paid < sale.total_price:
            cre_amount += 1
            cre_bal += sale.total_price - sale.total_amount_paid
    for sale in Sale.objects.all():
        actual_total_sales +=sale.total_price
    for dep in Depositor.objects.all():
        dep_bal += dep.balance
        dep_amount += 1
    for bor in Borrower.objects.all(): 
        bor_amount += 1
        bor_bal += bor.balance
    total_stock= 0
    stock_amount = 0
    stocks = Stock.objects.all() 
    
    for stock in stocks:
        stock_amount += stock.product.price * stock.quantity
        total_stock += stock.quantity
    stockamount = 0
    prod= Product.objects.all()
    for stock in Stock.objects.all():
        
        stockamount += stock.product.price * stock.quantity 
    t_eve= t_mob+t_ele+t_acc
    return render(request, 'admin/admin.html', {'bra_form':bra_form, 'all_total_amount_today':all_total_amount_today, 
    'stock_amount':stock_amount, 'total_stock':total_stock, 'actual_total_sales':actual_total_sales, 'num_today_cred':num_today_cred, 'total_amount_today':total_amount_today, 'today_total_profit':today_total_profit, 'today_cre_bal':today_cre_bal, 'num_today_sale':num_today_sale,
     'total_today_sale':total_today_sale, 'date':date, 'today_sales':today_sales, 't_eve':t_eve, 't_mob':t_mob,
     't_ele':t_ele,'t_acc':t_acc ,'cre_bal':cre_bal,'dep_bal':dep_bal,'bor_bal': bor_bal,'bor_amount':bor_amount, 
     'dep_amount':dep_amount,'cre_amount':cre_amount,'acc_amount':acc_amount,'mob_amount':mob_amount,
     'ele_amount':ele_amount,'total_sales':total_sales,'total_exp':total_exp,'total_balance':total_balance,
     'user_name':user_name,'top_dep':top_dep,'total_admins':total_admins,'total_cashiers':total_cashiers,
     'total_aux':total_aux,'total_users':total_users,'stk':stk,'prod_form':prod_form,'exp_form':exp_form, 
     'bor_form':bor_form, 'dep_form':dep_form,'total_accessories':total_accessories,'total_mobile':total_mobile,
     'total_electronic':total_electronic,'top_mob':top_mob,'top_acc':top_acc,'top_ele':top_ele})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_sale_payments(request,sid):
    exp_form = CashExpensesForm()
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    user_name = request.user.sup_user
    bal = sale.total_price - sale.total_amount_paid
    return render(request, 'admin/sale_payments.html', {'exp_form':exp_form, 'sid':sid, 'bal':bal,'user_name':user_name,'payments': payments,'title': 'Admin-Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def print_admin_invoice(request,pid):
    exp_form = CashExpensesForm()
    user_name = request.user.sup_user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    amount_paid = payment.total_amount
    sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'admin/invoice.html',{'exp_form':exp_form, 'balance':balance, 'amount_paid':amount_paid,'sale':sale,'user_name':user_name,'total_price': total_price,'sale':sale,'payment':payment})

 
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_products_report(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    quantity = 0
    brand_list = Product_Group.objects.all()
    
    prod_name =[]
    prod_quantity = []
    for ele in brand_list:
        prod_name.append(ele.product.name)
        prod_quantity.append(ele.quantity)
        
    prod_quant_lst = list(zip(prod_name, prod_quantity))
    
    prod_sorted = {}
    for key, value in prod_quant_lst:
        prod_sorted.setdefault(key, []).append(value)

    prod_quan_dict = {}
    for key, value in prod_sorted.items():
        prod_quan_dict[key] = sum(value)
    
    prod_lst = []
    quant_lst = []
    for pro, quant in prod_quan_dict.items():
        
        prod_lst.append(pro)
        quant_lst.append(quant)
    
    return render(request, 'admin/products_report.html',{
        'prod_quan_dict':zip(prod_lst, quant_lst),
         'brand_list':brand_list,  'stk':stk,'dep_form':dep_form, 'prod_form':prod_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_products_search_report(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    quantity = 0
    brand_list = Product_Group.objects.all()
    
    val_set = ''
    prod_sale = 0
    prod_no = 0
    
    if request.method == 'POST': 
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        prod_sales = Product_Group.objects.filter(date__date__lte=end,date__date__gte=start)
        for sale in prod_sales:
            prod_sale += sale.quantity
        prod_no = prod_sales.count()
        
    
    return render(request, 'admin/products_search_report.html',{
         'brand_list':brand_list,  'stk':stk,'dep_form':dep_form, 'prod_form':prod_form})


  
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_aux(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    staffs = Staff.objects.all()
    return render(request, 'admin/view_aux.html',{'user_name':user_name,'stk':stk,'staffs':staffs,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_receipt(request):
    bra_form = BrandForm()
    user_name = request.user.sup_user
    receipts = Receipt.objects.all()
    return render(request, 'admin/view_receipt.html',{'bra_form':bra_form, 'user_name':user_name,'receipts':receipts})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_brands(request):
    brands = Brand.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeven':
            bra_form = BrandForm(request.POST)
            if bra_form.is_valid():
               
                name = bra_form.cleaned_data['name']
                
                Brand.objects.create(name=name)
                messages.success(request, 'Success!! Brand created sucessfully')
                return redirect('/admin_view_brands/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'admin/view_brand.html',{'dep_form':dep_form, 'stk':stk , 'bra_form':bra_form, 'user_name':user_name,'brands':brands})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_invoice(request):
    user_name = request.user.sup_user
    invoices = Invoice.objects.all()
    return render(request, 'admin/view_invoice.html',{'user_name':user_name,'invoices':invoices})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_new_exp(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    exp_form = ExpenditureForm()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyFive':
            exp_form = ExpenditureForm(request.POST)
            if exp_form.is_valid():
                reciepient = exp_form.cleaned_data['reciepient'] 
                desc = exp_form.cleaned_data['desc'] 
                amount = exp_form.cleaned_data['amount']
                if int(amount)<0:
                    messages.warning(request, "!!!ERROR!!! Amount has to be greater than zero")
                else:
                    Expense.objects.create(reciepient=reciepient,desc=desc,amount=amount,date=timezone.now())
                    acc = Account.objects.all()[0]
                    acc.balance -= int(amount)
                    acc.save()
                    messages.success(request, 'Success!! New Expenditure added sucessfully')
                    return redirect('/admin_other_expenses/') 
    return render(request, 'admin/admin_new_exp.html',{'exp_form':exp_form,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_exp(request,eid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    exp = get_object_or_404(Expense,pk=eid)
    exp_form = ExpenditureForm(instance=exp)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyFive':
            exp_form = ExpenditureForm(request.POST)
            if exp_form.is_valid():
                reciepient = exp_form.cleaned_data['reciepient'] 
                desc = exp_form.cleaned_data['desc'] 
                amount = exp_form.cleaned_data['amount']
                if int(amount)<0:
                    messages.warning(request, "!!!ERROR!!! Amount has to be greater than zero")
                else:
                    amt = exp.amount
                    acc = Account.objects.all()[0]
                    acc.balance += int(amt)
                    exp.reciepient = reciepient
                    exp.desc = desc
                    exp.amount = amount
                    exp.save()
                    acc.balance -= int(amount)
                    acc.save()
                    messages.success(request, 'Success!! Expenditure updated sucessfully')
                    return redirect('/admin_other_expenses/') 
    return render(request, 'admin/admin_edit_exp.html',{'exp_form':exp_form,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_other_exp(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    expenses = Expense.objects.exclude(description='Total salary paid to deleted staff')
    user_name = request.user.sup_user
    val_set = ''
    total_amount = 0
    total_exp = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Expenitures from {start} to {end}'
        expenses = Expense.objects.filter(date__date__lte=end,date__date__gte=start).exclude(desc='Total salary paid to deleted staff')
        for exp in expenses:
            total_exp += 1
            total_amount += exp.amount
    return render(request, 'admin/other_expenditure.html',{'total_exp':total_exp,'val_set':val_set,'total_amount':total_amount,'expenses':expenses,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_pay_salaries(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    staffs = Staff.objects.all()
    total_salary = 0
    for staff in staffs:
        total_salary += staff.salary
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentysix':
            month = request.POST['month']
            year = request.POST['year']
            pay = month +'-'+year
            if Salaries.objects.filter(date=pay):
                messages.warning(request, f"!!!ERROR!!! Already logged salary for {pay}")
            else:
                for staff in staffs:
                    Salaries.objects.create(staff=staff,amount=staff.salary,date=pay)
                acc = Account.objects.all()[0]
                acc.balance -= total_salary
                acc.save()
                messages.success(request, 'Success!! Salary payments logged in sucessfully')
    paysal = Salaries.objects.all()
    return render(request, 'admin/admin_pay_salaries.html',{'paysal':paysal,'total_salary':total_salary,'staffs':staffs,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_aux_salary(request,aid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sname = get_object_or_404(Staff,pk=aid)
    salary = Salaries.objects.filter(staff=sname)
    return render(request, 'admin/view_aux_salary.html',{'salary':salary,'user_name':user_name,'sname':sname,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_users(request, uid=0):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sellers = Seller.objects.all()
    cashiers = Cashier.objects.all()
    admins = Sup_user.objects.all()
    cash = Cash.objects.all()
    return render(request, 'admin/view_users.html',{'cash':cash, 'user_name':user_name,'stk':stk,'sellers':sellers,'cashiers':cashiers,'admins':admins,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_aux(request):
    add_aux = AuxillaryForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThirteen':
            add_aux = AuxillaryForm(request.POST)
            if add_aux.is_valid():
                add_aux.save()
                messages.success(request, 'Success!! Staff created sucessfully')
                return redirect('/admin_view_aux/')
    return render(request, 'admin/add_aux.html',{'user_name':user_name,'stk':stk,'add_aux':add_aux,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_receipt(request):
    user_name = request.user.sup_user
    if request.method == 'POST':
        add_receipt = ReceiptForm(request.POST, request.FILES)
        if add_receipt.is_valid():
            company = add_receipt.cleaned_data['company']
            description = add_receipt.cleaned_data['description']
            image = add_receipt.cleaned_data['image']
            Receipt.objects.create(company=company,description=description, image=image)
            messages.success(request, 'Success!! Receipt created sucessfully')
            return redirect('/admin_view_receipt/')
    else:
        add_receipt=ReceiptForm()
        
   
    return render(request, 'admin/add_receipt.html', {'user_name':user_name, 'add_receipt':add_receipt})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_invoice(request):
    user_name = request.user.sup_user
    if request.method == 'POST':
        add_invoice = ReceiptForm(request.POST, request.FILES)
        if add_invoice.is_valid():
            company = add_invoice.cleaned_data['company']
            description = add_invoice.cleaned_data['description']
            image = add_invoice.cleaned_data['image']
            Invoice.objects.create(company=company,description=description, image=image)
            messages.success(request, 'Success!! invoice created sucessfully')
            return redirect('/admin_view_invoice/')
    else:
        add_invoice=InvoiceForm()
        
   
    return render(request, 'admin/add_invoice.html', {'user_name':user_name, 'add_invoice':add_invoice})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_statement(request):
    user_name = request.user.sup_user
    if request.method == 'POST':
        add_statement = StatementForm(request.POST, request.FILES)
        if add_statement.is_valid():
            name = add_statement.cleaned_data['name']
            subject = add_statement.cleaned_data['subject']
            statement = add_statement.cleaned_data['statement']
            Statement.objects.create(name=name,subject=subject, statement=statement)
            messages.success(request, 'Success!! Statement created sucessfully')
            return redirect('/admin_view_statements/')
    else:
        add_statement=StatementForm()
        
   
    return render(request, 'admin/add_statement.html', {'user_name':user_name, 'add_statement':add_statement})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_subject(request):
    user_name = request.user.sup_user
    if request.method == 'POST':
        add_subject = SubjectForm(request.POST, request.FILES)
        if add_subject.is_valid():
            name = add_subject.cleaned_data['name']
            
            Subject.objects.create(name=name)
            messages.success(request, 'Success!! Subject created sucessfully')
            return redirect('/admin_view_subjects/')
    else:
        add_subject=SubjectForm()
        
   
    return render(request, 'admin/add_subject.html', {'user_name':user_name, 'add_subject':add_subject})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_statements(request):
    val_set = ''
    state_no = 0
    dep_form = DepositorForm()
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    state_form = StatementForm()
    statements = Statement.objects.all()
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Statements from {start} to {end}'
        statements = Statement.objects.filter(date__date__lte=end,date__date__gte=start)
        state_no = statements.count()
    return render(request, 'admin/admin_view_statements.html', {'dep_form':dep_form, 'statements':statements,
    'exp_form':exp_form,'state_no':state_no,'val_set':val_set, 'bor_form':bor_form,'prod_form':prod_form,'bra_form':bra_form,'state_form':state_form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_subjects(request):
    
    dep_form = DepositorForm()
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    state_form = StatementForm()
    subjects = Subject.objects.all()
    
    return render(request, 'admin/admin_view_subjects.html', {'dep_form':dep_form, 'subjects':subjects,
    'exp_form':exp_form, 'bor_form':bor_form,'prod_form':prod_form,'bra_form':bra_form,'state_form':state_form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_statement_reciept(request,sid):
    
    statement = get_object_or_404(Statement,pk=sid)
    # total_price = payment.sale.total_price
    # amount_paid = payment.total_amount
    # balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.sup_user

    return render(request, 'admin/admin_statement_reciept.html', {
        # 'amount_paid':amount_paid,'mob_sale':mob_sale,'payment':payment,'balance':balance,
         'statement':statement, 
         'user_name':user_name,'title': 'Print Invoice'})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_statement(request,sid):
    obj = get_object_or_404(Statement,pk=sid)
    state_form = StatementUpdateForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
            state_form = StatementUpdateForm(request.POST, instance=obj)
            if state_form.is_valid():
                state_form.save()
                messages.success(request, 'Success!! Staff updated sucessfully')
                return redirect('/admin_view_statements/')
    return render(request, 'admin/edit_statement.html',{'user_name':user_name,'stk':stk,'state_form':state_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_subject(request,sid):
    obj = get_object_or_404(Subject,pk=sid)
    subj_form = SubjectUpdateForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
            subj_form = SubjectUpdateForm(request.POST, instance=obj)
            if subj_form.is_valid():
                subj_form.save()
                messages.success(request, 'Success!! Subject updated sucessfully')
                return redirect('/admin_view_subjects/')
    return render(request, 'admin/edit_subject.html',{'user_name':user_name,'stk':stk,'subj_form':subj_form,'prod_form':prod_form,'dep_form':dep_form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_aux(request,aid):
    obj = get_object_or_404(Staff,pk=aid)
    edit_aux = AuxillaryForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFourteen':
            edit_aux = AuxillaryForm(request.POST, instance=obj)
            if edit_aux.is_valid():
                edit_aux.save()
                messages.success(request, 'Success!! Staff updated sucessfully')
                return redirect('/admin_view_aux/')
    return render(request, 'admin/edit_aux.html',{'user_name':user_name,'stk':stk,'edit_aux':edit_aux,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_user(request):
    reg_form = UserForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formThree':
            reg_form = UserForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                email = reg_form.cleaned_data['email']
                fname = reg_form.cleaned_data['fname']
                lname = reg_form.cleaned_data['lname']
                user_type = request.POST['user_type']
                telephone = reg_form.cleaned_data['telephone']
                password = reg_form.cleaned_data['password1']
                obj = get_object_or_404(User,email=email)
                if user_type == 'acc' or user_type == 'ele' or user_type == 'mob':
                    if user_type == 'acc':
                        Seller.objects.create(user=obj,fname=fname,lname=lname,type=user_type,telephone=telephone)
                        group = Group.objects.get(name='accessory')
                        user.groups.add(group)
                    elif user_type == 'ele':
                        Seller.objects.create(user=obj,fname=fname,lname=lname,type=user_type,telephone=telephone)
                        group = Group.objects.get(name='electronic')
                        user.groups.add(group)
                    elif user_type == 'mob':
                        Seller.objects.create(user=obj,fname=fname,lname=lname,type=user_type,telephone=telephone)
                        group = Group.objects.get(name='mobile')
                        user.groups.add(group)
                elif user_type == 'cas':
                    Cashier.objects.create(user=obj,fname=fname,lname=lname,telephone=telephone)
                    group = Group.objects.get(name='cashier')
                    user.groups.add(group)
                elif user_type == 'cash':
                    Cash.objects.create(user=obj,fname=fname,lname=lname,telephone=telephone)
                    group = Group.objects.get(name='cash')
                    user.groups.add(group)
                elif user_type == 'adm':
                    Sup_user.objects.create(user=obj,fname=fname,lname=lname,telephone=telephone)
                    group = Group.objects.get(name='admin')
                    user.groups.add(group)
                messages.success(request, 'Success!! Account created sucessfully')
                return redirect('/admin_view_users/')
    return render(request, 'admin/add_user.html',{'user_name':user_name,'stk':stk,'reg_form':reg_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_seller_stock(request,pid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sel_list =  Stock.objects.filter(product__id=pid)
    prod = get_object_or_404(Product,pk=pid)
    return render(request, 'admin/seller_stock.html', {'user_name':user_name,'stk':stk,'prod':prod,'pid':pid,'prod_form':prod_form,'dep_form':dep_form,'sel_list': sel_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_seller(request,uid):
    sel = get_object_or_404(Seller,pk=uid)
    sel_form = UpdateSellerForm(instance=sel)
    obj = get_object_or_404(User,email=sel.user.email)
    usr_form = UpdateUserForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEleven':
            usr_form = UpdateUserForm(request.POST, instance=obj)
            sel_form = UpdateSellerForm(request.POST)
            if usr_form.is_valid() and sel_form.is_valid():
                sel.fname = sel_form.cleaned_data['fname']
                sel.lname = sel_form.cleaned_data['lname']
                sel.telephone = sel_form.cleaned_data['telephone']
                sel.save()
                usr_form.save()
                obj.set_password(usr_form.cleaned_data['password1'])
                obj.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_users/')
    return render(request, 'admin/edit_seller.html',{'user_name':user_name,'stk':stk,'sel_form':sel_form,'usr_form':usr_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_cashier(request,uid):
    cas = get_object_or_404(Cashier,pk=uid)
    cas_form = UpdateCashierForm(instance=cas)
    obj = get_object_or_404(User,email=cas.user.email)
    usr_form = UpdateUserForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formNine':
            usr_form = UpdateUserForm(request.POST, instance=obj)
            cas_form = UpdateCashierForm(request.POST)
            if usr_form.is_valid() and cas_form.is_valid():
                cas.fname = cas_form.cleaned_data['fname']
                cas.lname = cas_form.cleaned_data['lname']
                cas.telephone = cas_form.cleaned_data['telephone']
                cas.save()
                usr_form.save()
                obj.set_password(usr_form.cleaned_data['password1'])
                obj.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_users/')
    return render(request, 'admin/edit_cashier.html',{'user_name':user_name,'stk':stk,'cas_form':cas_form,'usr_form':usr_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_admin(request,uid):
    adm = get_object_or_404(Sup_user,pk=uid)
    adm_form = UpdateAdminForm(instance=adm)
    obj = get_object_or_404(User,email=adm.user.email)
    usr_form = UpdateUserForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTen':
            usr_form = UpdateUserForm(request.POST, instance=obj)
            adm_form = UpdateAdminForm(request.POST)
            if usr_form.is_valid() and adm_form.is_valid():
                adm.fname = adm_form.cleaned_data['fname']
                adm.lname = adm_form.cleaned_data['lname']
                adm.telephone = adm_form.cleaned_data['telephone']
                adm.save()
                usr_form.save()
                obj.set_password(usr_form.cleaned_data['password1'])
                obj.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_users/')
    return render(request, 'admin/edit_admin.html',{'user_name':user_name,'usr_form':usr_form,'adm_form':adm_form,'stk':stk,'prod_form':prod_form,'dep_form':dep_form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_depositors(request):
    depositor_list = Depositor.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            dep_form = DepositorForm(request.POST)
            if dep_form.is_valid():
                amt = dep_form.cleaned_data['balance']
                acc = Account.objects.all()[0]
                acc.balance += int(amt)
                acc.save()
                dep = dep_form.save()
                Transaction.objects.create(depositor=dep,action='Deposit',amount=amt,date=timezone.now())
                messages.success(request, 'Success!! Depositor created sucessfully')
                return redirect('/admin_view_depositors/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'admin/view_depositors.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_cash_depositors(request):
    depositor_list = CashDepositor.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    total_amount = 0
    no_depositors = 0
    for amount in CashBorrower.objects.all():
        total_amount += amount.balance
    no_depositors =  CashDepositor.objects.all().count() 
    # if request.method == 'POST':
    #     if request.POST.get("form_type") == 'formOne':
    #         dep_form = DepositorForm(request.POST)
    #         if dep_form.is_valid():
    #             amt = dep_form.cleaned_data['balance']
    #             acc = Account.objects.all()[0]
    #             acc.balance += int(amt)
    #             acc.save()
    #             dep = dep_form.save()
    #             Transaction.objects.create(depositor=dep,action='Deposit',amount=amt,date=timezone.now())
    #             messages.success(request, 'Success!! Depositor created sucessfully')
    #             return redirect('/admin_view_depositors/')
    #         else:
    #             messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'admin/admin_view_cash_depositors.html', {'total_amount':total_amount,'no_depositors':no_depositors, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_cash_borrowers(request):
    borrower_list = CashBorrower.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    total_amount = 0
    no_borrowers = 0
    for amount in CashBorrower.objects.all():
        total_amount += amount.balance
    no_borrowers =  CashBorrower.objects.all().count()  
    # if request.method == 'POST':
    #     if request.POST.get("form_type") == 'formOne':
    #         dep_form = DepositorForm(request.POST)
    #         if dep_form.is_valid():
    #             amt = dep_form.cleaned_data['balance']
    #             acc = Account.objects.all()[0]
    #             acc.balance += int(amt)
    #             acc.save()
    #             dep = dep_form.save()
    #             Transaction.objects.create(depositor=dep,action='Deposit',amount=amt,date=timezone.now())
    #             messages.success(request, 'Success!! Depositor created sucessfully')
    #             return redirect('/admin_view_depositors/')
    #         else:
    #             messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'admin/admin_view_cash_borrowers.html', {'bra_form':bra_form, 'no_borrowers':no_borrowers, 'total_amount':total_amount, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'borrower_list': borrower_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_recorded_sales(request):
    depositor_list = Depositor.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    record_sales = RecordedSale.objects.all()
    total_amount = 0
    no_borrowers = 0
    for amount in record_sales:
        total_amount += amount.amount
    no_sales =  record_sales.count() 

    return render(request, 'admin/view_recorded_sales.html', {'total_amount':total_amount,'no_sales':no_sales, 'record_sales':record_sales, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_savings(request):
    depositor_list = Depositor.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    savings = Saving.objects.all()

    return render(request, 'admin/admin_view_savings.html', {'savings':savings, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_cash_expenses(request):
    depositor_list = Depositor.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    expenses = CashExpense.objects.all()
    total_amount = 0
    no_expense = 0
    for amount in expenses:
        total_amount += amount.amount
    no_expense =  expenses.count()
    return render(request, 'admin/admin_view_cash_expenses.html', {'total_amount':total_amount,'no_expense':no_expense, 'expenses':expenses, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_depositor(request,did):
    dep = get_object_or_404(Depositor,pk=did)
    up_dep = UpdateDepositorForm(instance=dep)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            up_dep = UpdateDepositorForm(request.POST,instance=dep)
            if up_dep.is_valid():
                up_dep.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_depositors/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    depositor_list = Depositor.objects.all()
    return render(request, 'admin/edit_depositor.html', {'user_name':user_name,'stk':stk,'up_dep':up_dep,'prod_form':prod_form,'dep_form':dep_form,'depositor_list': depositor_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_borrowers(request):
    borrower_list = Borrower.objects.all()
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
            bor_form = BorrowerForm(request.POST)
            if bor_form.is_valid():
                amt = bor_form.cleaned_data['balance']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = bor_form.save()
                    Borrower_Transaction.objects.create(borrower=dep,action='Borrower',amount=amt,date=timezone.now())
                    messages.success(request, 'Success!! Borrower created sucessfully')
                    return redirect('/admin_view_borrowers/')
                else:
                    messages.warning(request, 'Error!! Borrow cannot be More than the balance')
                    return redirect('/admin_view_borrowers/')
            else:
                messages.warning(request, 'Error!! Borrower cannot Borrow more than the company balance')
            return redirect('/admin_view_borrowers/')
           
    return render(request, 'admin/view_borrowers.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'borrower_list': borrower_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_salaries(request):
    salary_list = Salaries.objects.all()
    
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    sal_form = SalaryForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEightyTwo':
            sal_form = SalaryForm(request.POST)
            if sal_form.is_valid():
                amt = sal_form.cleaned_data['amount']
                month =  sal_form.cleaned_data['month']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = sal_form.save()
                    Salary_Transaction.objects.create(salary=dep,action='Payment',amount=amt,month=month, date=timezone.now())
                    messages.success(request, 'Success!! Salary created sucessfully')
                    return redirect('/admin_view_salaries/')
                else:
                    messages.warning(request, 'Error!! Salary cannot be More than the balance')
                    return redirect('/admin_view_salaries/')
            else:
                messages.warning(request, 'Error!! Salary cannot Paid more than the company balance')
            return redirect('/admin_view_salaries/')
           
    return render(request, 'admin/view_salaries.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'sal_form':sal_form,'salary_list': salary_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def borrowers_today(request):
    date = timezone.now().date()
    borrower_list = Borrower_Transaction.objects.filter(date__date=date)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()

    user_name = request.user.sup_user
           
    return render(request, 'admin/borrowers_today.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'borrower_list': borrower_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def depositors_today(request):
    date = timezone.now().date()
    depositor_list = Transaction.objects.filter(date__date=date)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    dep_form = DepositorForm()
    user_name = request.user.sup_user      
    return render(request, 'admin/depositors_today.html', {'exp_form':exp_form,'dep_form':dep_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'depositor_list': depositor_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def sales_today(request):
    date = timezone.now().date()
    sales_list = Sale.objects.filter(date__date=date)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
           
    return render(request, 'admin/sales_today.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def creditors_today(request):
    date = timezone.now().date()
    sales_list = Sale.objects.filter(date__date=date)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
           
    return render(request, 'admin/creditors_today.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def expenses_today(request):
    date = timezone.now().date()
    expenses_list = Expenses.objects.filter(date__date=date)
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
           
    return render(request, 'admin/expenses_today.html', {'exp_form':exp_form, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'expenses_list': expenses_list})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_salary(request,sid):
    sal = get_object_or_404(Salaries,pk=sid)
    up_sal = UpdateSalaryForm(instance=sal)
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
            up_sal = UpdateSalaryForm(request.POST,instance=sal)
            if up_sal.is_valid():
                up_sal.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_salaries/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    salary_list = Salaries.objects.all()
    return render(request, 'admin/edit_salary.html', {'user_name':user_name,'stk':stk,'up_sal':up_sal,'prod_form':prod_form,'bor_form':bor_form,'salary_list': salary_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def salary_transactions(request,sal_pk):
    stk = Stock.objects.filter(quantity=0)
    sal_form = SalaryForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sal_trans = Salary_Transaction.objects.filter(salary_id=sal_pk)
    sal = get_object_or_404(Salaries,pk=sal_pk)
    salname = sal.staff.fname + ' ' + sal.staff.lname
    val_set = ''
    total_amt = 0
    total_ref = 0
    total_pay = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transaction for {salname} from {start} to {end}'
        sal_trans = Salary_Transaction.objects.filter(salary_id=sal_pk,date__date__lte=end,date__date__gte=start)
        for trans in sal_trans:
            total_amt += 1
            if trans.action == 'Payment':
                total_pay += trans.amount
            elif trans.action == 'Refund':
                total_ref += trans.amount

    return render(request, 'admin/salary_transactions.html', { 'val_set':val_set,'total_amt':total_amt,'total_ref':total_ref,'total_pay':total_pay,'user_name':user_name,'stk':stk,'prod_form':prod_form,'sal_form':sal_form,'sal_trans': sal_trans,'sal': sal, 'salname':salname})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def salary_payment(request,sid):
    pay_form = SalForm()
    stk = Stock.objects.filter(quantity=0)
    sal_form = SalaryForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEightyNine':
                pay_form = SalForm(request.POST)
                if pay_form.is_valid():
                    amount = pay_form.cleaned_data['amount']
                    month = pay_form.cleaned_data['month']
                    dep = get_object_or_404(Salaries,pk=sid)
                    if amount >= 0:
                        if amount <= acc.balance:
                            dep.amount = F('amount') + amount
                            dep.save()
                            trans = Salary_Transaction.objects.create(salary=dep,action='Payment',amount=amount, month=month,date=timezone.now())
                        
                        
                            acc.balance -= int(amount)
                            acc.save()
                            messages.success(request, 'Success!! Transaction completed sucessfully')
                        else:
                             messages.warning(request, 'Error!! Transaction Fail, Amount Cant be Greater than Company balance')
                        return redirect(f'/admin_salary_transactions/{sid}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed Amount Can't be less than Zero")
                    return redirect(f'/admin_salary_transactions/{sid}/')
    sales_list = Sale.objects.all()
    return render(request, 'admin/salary_payment.html', {'user_name':user_name,'sid':sid,'stk':stk,'sal_form':sal_form,'prod_form':prod_form,'pay_form':pay_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_expenses(request):
    expenses_list = CashExpenses.objects.all()
    stk = Stock.objects.filter(quantity=0)
    exp_form = CashExpensesForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    acc = CashAccount.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formNine':
            exp_form = CashExpensesForm(request.POST)
            if exp_form.is_valid():
                amt = exp_form.cleaned_data['balance']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = exp_form.save()
                    CashExpenses_Transaction.objects.create(expense=dep,action='Expense',amount=amt,date=timezone.now())
                    messages.success(request, 'Success!! Expense created sucessfully')
                    return redirect('/admin_view_expenses/')
                else:
                    messages.warning(request, 'Error!! Borrow cannot be More than the balance')
                    return redirect('/admin_view_expenses/')
            else:
                messages.warning(request, 'Error!! Borrower cannot Borrow more than the company balance')
            return redirect('/admin_view_expenses/')
           
    return render(request, 'admin/view_CashExpenses.html', {'exp_form':exp_form, 
    'user_name':user_name,'stk':stk,
    'prod_form':prod_form,'bor_form':bor_form, 'bra_form':bra_form,
    'expenses_list': expenses_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_shop_expenses(request):
    expenses_list = Expense.objects.all()
    salaries = Salaries.objects.all()
    salary = 0
    expenses = 0
    for sal in salaries:
        salary += sal.amount
    for ex in expenses_list:
        expenses += ex.balance
    stk = Stock.objects.filter(quantity=0)
    exp_form = ExpenditureForm()
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentySix':
            exp_form = ExpenditureForm(request.POST)
            if exp_form.is_valid():
                amt = exp_form.cleaned_data['balance']
                if amt <= acc.balance:
                    acc.balance -= int(amt) 
                    acc.save()
                    dep = exp_form.save()
                    Expense_Transaction.objects.create(expense=dep,action='Expense',amount=amt,date=timezone.now())
                    messages.success(request, 'Success!! Expense created sucessfully')
                    return redirect('/admin_view_shop_expenses/')
                else:
                    messages.warning(request, 'Error!! Withdraw cannot be More than the balance')
                    return redirect('/admin_view_shop_expenses/')
            else:
                messages.warning(request, 'Error!! Expenses cannot be more than the company balance')
            return redirect('/admin_view_shop_expenses/')
           
    return render(request, 'admin/view_Expenses.html', {'expenses':expenses, 'salary':salary, 'exp_form':exp_form, 
    'user_name':user_name,'stk':stk,
    'prod_form':prod_form,'bor_form':bor_form, 'bra_form':bra_form,
    'expenses_list': expenses_list})




@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_stock(request):
    # borrower_list = Borrower.objects.all()
    stocks = Stock.objects.all()
    user_name = request.user.sup_user
    bra_form = BrandForm()
          
    return render(request, 'admin/admin_view_stock.html', {'bra_form':bra_form, 'user_name':user_name,'stocks':stocks})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def borrower_reciept(request,bid):
    user_name = request.user
    bra_form = BrandForm()
    borrower = get_object_or_404(Borrower_Transaction,pk=bid)
    return render(request, 'admin/borrower_reciept.html', {'bra_form':bra_form, 'borrower':borrower, 'user_name':user_name, 'title': 'Print Reciept'})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def salary_reciept(request,sid):
    user_name = request.user
    bra_form = BrandForm()
    salary = get_object_or_404(Salary_Transaction,pk=sid)
    return render(request, 'admin/salary_reciept.html', {'bra_form':bra_form, 'salary':salary, 'user_name':user_name, 'title': 'Print Reciept'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def depositor_reciept(request,did):
    user_name = request.user
    depositor = get_object_or_404(Transaction,pk=did)
    return render(request, 'admin/depositor_reciept.html', {'depositor':depositor, 'user_name':user_name, 'title': 'Print Reciept'})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_borrower(request,bid):
    bor = get_object_or_404(Borrower,pk=bid)
    up_bor = UpdateBorrowerForm(instance=bor)
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFourtty':
            up_bor = UpdateBorrowerForm(request.POST,instance=bor)
            if up_bor.is_valid():
                up_bor.save()
                messages.success(request, 'Success!! Account updated sucessfully')
                return redirect('/admin_view_borrowers/')
            else:
                messages.warning(request,'!!!ERROR!!! Try Again')
    borrower_list = Borrower.objects.all()
    return render(request, 'admin/edit_borrower.html', {'user_name':user_name,'stk':stk,'up_bor':up_bor,'prod_form':prod_form,'bor_form':bor_form,'borrower_list': borrower_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def borrower_repay(request,bid):
    rep_form = RepayForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeventy':
                rep_form = RepayForm(request.POST)
                if rep_form.is_valid():
                    amount = rep_form.cleaned_data['amount']
                    description=rep_form.cleaned_data['description']
                    dep = get_object_or_404(Borrower,pk=bid)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = Borrower_Transaction.objects.create(borrower=dep,action='Repay',amount=amount, description=description, date=timezone.now())
                        acc = Account.objects.all()[0]
                        acc.balance += int(amount)  
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                    else:
                         messages.warning(request, '!!!Error!!! Transaction Fail!! Amount Cant be greater than Balance')
                    return redirect(f'/admin_borrower_transactions/{bid}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'admin/borrower_repay.html', { 'user_name':user_name,'bid':bid,'stk':stk,'rep_form':rep_form,'prod_form':prod_form,'bor_form':bor_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def borrower_borrowed(request,bid):
    wit_form = BorrowForm()
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    acc = Account.objects.all()[0]
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighty':
                wit_form = BorrowForm(request.POST)
                if wit_form.is_valid():
                    amount = wit_form.cleaned_data['amount']
                    description = wit_form.cleaned_data['description']
                    dep = get_object_or_404(Borrower,pk=bid)
                    if amount >= 0:
                        if amount <= acc.balance:
                            dep.balance = F('balance') + amount
                            dep.save()
                            trans = Borrower_Transaction.objects.create(borrower=dep,action='Borrow',amount=amount, description=description,date=timezone.now())
                        
                        
                            acc.balance -= int(amount)
                            acc.save()
                            messages.success(request, 'Success!! Transaction completed sucessfully')
                        else:
                             messages.warning(request, 'Error!! Transaction Fail, Amount Cant be Greater than Company balance')
                        return redirect(f'/admin_borrower_transactions/{bid}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed Amount Can't be less than Zero")
                    return redirect(f'/admin_borrower_transactions/{bid}/')
    sales_list = Sale.objects.all()
    return render(request, 'admin/borrower_borrowed.html', {'user_name':user_name,'bid':bid,'stk':stk,'bor_form':bor_form,'prod_form':prod_form,'wit_form':wit_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def borrower_transactions(request,bor_pk):
    stk = Stock.objects.filter(quantity=0)
    bor_form = BorrowerForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    bor_trans = Borrower_Transaction.objects.filter(borrower_id=bor_pk)
    bor = get_object_or_404(Borrower,pk=bor_pk)
    borname = bor.fname + ' ' + bor.lname
    val_set = ''
    total_amt = 0
    total_rep = 0
    total_bor = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transaction for {borname} from {start} to {end}'
        bor_trans = Borrower_Transaction.objects.filter(borrower_id=bor_pk,date__date__lte=end,date__date__gte=start)
        for trans in bor_trans:
            total_amt += 1
            if trans.action == 'Borrow':
                total_bor += trans.amount
            elif trans.action == 'Repay':
                total_rep += trans.amount

    return render(request, 'admin/borrower_transactions.html', { 'val_set':val_set,'total_amt':total_amt,'total_rep':total_rep,'total_bor':total_bor,'user_name':user_name,'stk':stk,'prod_form':prod_form,'bor_form':bor_form,'bor_trans': bor_trans,'bor': bor, 'borname':borname})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_products(request):
    product_list = Product.objects.all()
    bra_list = Brand.objects.all()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwo':
            prod_form = ProductForm(request.POST)
            if prod_form.is_valid():
                category = request.POST['category']
                name = prod_form.cleaned_data['name']
                brand = prod_form.cleaned_data['brand']
                price = prod_form.cleaned_data['price']
                desc = prod_form.cleaned_data['desc']
                total_quantity = prod_form.cleaned_data['total_quantity']
                Product.objects.create(category=category,name=name,brand=brand,price=price,desc=desc,total_quantity=total_quantity)
                messages.success(request, 'Success!! Product created sucessfully')
                return redirect('/admin_view_products/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    return render(request, 'admin/view_products.html', {'bra_list':bra_list, 'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'product_list': product_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def add_product_stock(request,pid):
    prod = get_object_or_404(Product,pk=pid)
    edit_prod = Seller.objects.filter(type=prod.category,user__is_active=True)
    selstok_form = RestockForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    bra_form = BrandForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwelve':
                selstok_form = RestockForm(request.POST)
                if selstok_form.is_valid():
                    seller = get_object_or_404(Seller,pk=request.POST['seller'])
                    quantity = selstok_form.cleaned_data['quantity']
                    if Stock.objects.filter(product=prod,seller=seller).exists():
                        messages.warning(request, "!!!ERROR!!! Seller already has inventory for product. Update inventory instead")
                    else:
                        if quantity <= prod.total_quantity:
                            prod.total_quantity = F('total_quantity') - quantity
                            prod.save()
                            s = Stock.objects.create(seller=seller,product=prod,quantity=quantity)
                            messages.success(request, f'Success!! {prod.name} stock created for {seller} sucessfully')
                            return redirect(f'/admin_seller_stock/{pid}/')
                        else:
                            messages.warning(request, "!!!ERROR!!! Quantity assigned to seller's inventory more than amount in stock")
                else:
                    messages.warning(request, "!!!ERROR!!! Try Again")
    product_list = Product.objects.all()
    return render(request, 'admin/seller_stock_create.html', {'bra_form':bra_form, 'user_name':user_name,'selstok_form':selstok_form,'pid':pid,'stk':stk,'edit_prod':edit_prod,'prod_form':prod_form,'dep_form':dep_form,'product_list': product_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_product_stock(request,pid,sid):
    res_form = RestockForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSix':
                res_form = RestockForm(request.POST)
                if res_form.is_valid():
                    quantity = res_form.cleaned_data['quantity']
                    s = get_object_or_404(Stock,seller__id=sid,product__id=pid)
                    prod = get_object_or_404(Product,pk=pid)
                    if int(quantity) <= prod.total_quantity:
                        prod.total_quantity = F('total_quantity') - quantity
                        prod.save()
                        s.quantity = F('quantity') + quantity
                        s.save()
                        messages.success(request, 'Success!! Stock updated sucessfully')
                        return redirect(f'/admin_seller_stock/{pid}/')
                    else:
                        messages.warning(request, "!!!ERROR!!! Quantity assigned to seller's inventory more than amount in stock")
                else:
                    messages.warning(request, "!!!ERROR!!! Try Again with a legal value")
    product_list = Product.objects.all()
    return render(request, 'admin/edit_product_stock.html', {'bra_form':bra_form ,'user_name':user_name,'stk':stk,'res_form':res_form,'prod_form':prod_form,'dep_form':dep_form,'product_list': product_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_product_stock(request,pid):
    rest_form = ProductRestockForm()
    obj = get_object_or_404(Product,pk=pid)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwentyfour':
                rest_form = ProductRestockForm(request.POST,instance=obj)
                if rest_form.is_valid():
                    quantity = request.POST['total_quantity']
                    # if int(quantity) > 0:
                    obj.total_quantity = F('total_quantity') + quantity
                    obj.save()
                    messages.success(request, 'Success!! Stock updated sucessfully')
                    return redirect('/admin_view_products/')
                    # else:
                    #     messages.warning(request, '!!!ERROR!!! Enter a valid number')
                else:
                    messages.warning(request, "!!!ERROR!!! Try Again with a legal value")
    return render(request, 'admin/edit_product_stock_quantity.html', {'bra_form':bra_form, 'user_name':user_name,'stk':stk,'rest_form':rest_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_product(request,pid):
    prod = get_object_or_404(Product,pk=pid)
    up_prod = ProductUpdateForm(instance=prod)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    brand_list = Brand.objects.all()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFive':
            up_prod = ProductUpdateForm(request.POST,instance=prod)
            if up_prod.is_valid():
                up_prod.save()
                messages.success(request, 'Success!! Product updated sucessfully')
                return redirect(f'/admin_view_products/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    product_list = Product.objects.all()
    return render(request, 'admin/edit_product.html', {'bra_form':bra_form, 'brand_list':brand_list, 'user_name':user_name,'stk':stk,'up_prod':up_prod,'prod_form':prod_form,'dep_form':dep_form,'product_list': product_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def edit_brand(request,bid):
    bra = get_object_or_404(Brand, pk=bid)
    up_bra = UpdateBrandForm(instance=bra)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formNine':
            up_bra =UpdateBrandForm(request.POST,instance=bra)
            if up_bra.is_valid():
                up_bra.save()
                messages.success(request, 'Success!! Brand updated sucessfully')
                return redirect(f'/admin_view_brands/')
            else:
                messages.warning(request, "!!!ERROR!!! Try Again")
    product_list = Product.objects.all()
    return render(request, 'admin/edit_brand.html', {'user_name':user_name,'up_bra':up_bra,'prod_form':prod_form,'dep_form':dep_form,'product_list': product_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def depositor_deposit(request,did):
    des_form = DepositForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formSeven':
                des_form = DepositForm(request.POST)
                if des_form.is_valid():
                    amount = des_form.cleaned_data['amount']
                    description = des_form.cleaned_data['description']
                    dep = get_object_or_404(Depositor,pk=did)
                    dep.balance = F('balance') + amount
                    dep.save()
                    trans = Transaction.objects.create(depositor=dep,action='Deposit',amount=amount,description=description,  date=timezone.now())
                    acc = Account.objects.all()[0]
                    acc.balance += int(amount)
                    acc.save()
                    messages.success(request, 'Success!! Transaction completed sucessfully')
                    return redirect(f'/admin_depositor_transactions/{did}/')
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")  
    sales_list = Sale.objects.all()
    return render(request, 'admin/depositor_deposit.html', {'user_name':user_name,'did':did,'stk':stk,'des_form':des_form,'prod_form':prod_form,'dep_form':dep_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def depositor_withdraw(request,did):
    wit_form = WithdrawForm()
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEight':
                wit_form = WithdrawForm(request.POST)
                if wit_form.is_valid():
                    amount = wit_form.cleaned_data['amount']
                    description = wit_form.cleaned_data['description']
                    dep = get_object_or_404(Depositor,pk=did)
                    if amount <= dep.balance:
                        dep.balance = F('balance') - amount
                        dep.save()
                        trans = Transaction.objects.create(depositor=dep,action='Withdraw',amount=amount ,description=description,date=timezone.now())
                        acc = Account.objects.all()[0]
                        acc.balance -= int(amount)
                        acc.save()
                        messages.success(request, 'Success!! Transaction completed sucessfully')
                        return redirect(f'/admin_depositor_transactions/{did}/')
                    else:
                        messages.warning(request, "!!!Transaction Failed!!! Insufficient Funds!! Enter a legal amount")
                else:
                    messages.warning(request, "!!!ERROR!!! Transaction Failed")
                    return redirect(f'/admin_depositor_transactions/{did}/')
    sales_list = Sale.objects.all()
    return render(request, 'admin/depositor_withdraw.html', {'user_name':user_name,'did':did,'stk':stk,'wit_form':wit_form,'prod_form':prod_form,'dep_form':dep_form,'sales_list': sales_list})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_creditor_product(request,sid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'admin/admin_creditor_product.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'sales_prod': sales_prod})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_sale_product(request,sid):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'admin/admin_view_sale_product.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'sales_prod': sales_prod})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_reports(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    bra_form = BrandForm()
    user_name = request.user.sup_user
    val_set = ''
    total_amount = 0
    total_price = 0
    total_profit = 0
    total_cre = 0
    sale_no = 0
    cre_bal=0
    cre_amount=0
    sales_list = Sale.objects.all()
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        sales_list = Sale.objects.filter(date__date__lte=end,date__date__gte=start)
        for sale in sales_list:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
            total_profit += (sale.total_price - sale.actual_total_price)
        # for sale in Sale.objects.all():
            if sale.total_amount_paid < sale.total_price:
                cre_amount += 1
                cre_bal += sale.total_price - sale.total_amount_paid
        sale_no = sales_list.count()
    return render(request, 'admin/view_sales.html', {'bra_form':bra_form, 'cre_bal':cre_bal, 'total_profit':total_profit,'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'sales_list': sales_list})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_cash_athand(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    
    t_sale_no = 0
    t_sale_amount = 0
    t_dep_no = 0
    t_dep_amount = 0
    t_bor_no = 0
    t_bor_amount=0
    t_exp_no=0
    t_exp_amount =0

    sale_no = 0
    sale_amount = 0
    dep_no = 0
    dep_amount = 0
    bor_no = 0
    bor_amount=0
    exp_no=0
    exp_amount=0
    t_cre_amount = 0
    t_cre_bal = 0
    cre_amount = 0
    cre_bal = 0
    date = timezone.now().date()
    sales = Sale.objects.filter(date__date=date)
    sales1 = Sale.objects.all()
    deposits = Transaction.objects.filter(date__date=date)
    deposits1 = Depositor.objects.all()
    borrowers = Borrower_Transaction.objects.filter(date__date=date)
    borrowers1 = Borrower.objects.all()
    expenses = Expense.objects.filter(date__date=date)
    expenses1 = Expense.objects.all()
    for sale in Sale.objects.all():
        if sale.total_amount_paid < sale.total_price:
            cre_amount += 1
            cre_bal += sale.total_price - sale.total_amount_paid
    for sale in Sale.objects.filter(date__date=date):
        if sale.total_amount_paid < sale.total_price:

            t_cre_amount += 1
            t_cre_bal += sale.total_price - sale.total_amount_paid
    # for payment in Payment.objects.filter(date__date=date):
    #     t_cre_amount +=1
    #     t_cre_bal += payment.balance
    for sale in sales: 
        t_sale_amount += sale.total_price
    t_sale_no = sales.count()
    for sale in sales1:
        sale_amount += sale.total_price
    sale_no = sales1.count()
    for deposit in deposits: 
        t_dep_amount += deposit.amount
    t_dep_no = deposits.count()
    for deposit in deposits1:
        dep_amount += deposit.balance
    dep_no = deposits1.count()
    for borrower in borrowers: 
        t_bor_amount += borrower.amount
    t_bor_no = borrowers.count()
    for borrower in borrowers1:
        bor_amount += borrower.balance
        
    bor_no = borrowers1.count()
    for expense in expenses: 
        t_exp_amount += expense.balance
    t_exp_no = expenses.count()
    for expense in expenses1:
        exp_amount += expense.balance
    exp_no = expenses1.count()

    return render(request, 'admin/admin_cash_athand.html', {'t_sale_no':t_sale_no, 
    't_sale_amount':t_sale_amount,
    't_dep_no' :t_dep_no,
    't_dep_amount' :t_dep_amount,
    't_bor_no':t_bor_no,
    't_bor_amount':t_bor_amount,
    't_exp_amount':t_exp_amount,
    't_exp_no':t_exp_no,
    't_cre_amount' :t_cre_amount ,
    't_cre_bal':t_cre_bal,
    'cre_amount' :cre_amount ,
    'cre_bal':cre_bal,
    'sale_no':sale_no,
    'sale_amount' :sale_amount,
    'dep_no' : dep_no,
    'dep_amount':dep_amount,
    'bor_no' : bor_no,
    'bor_amount':bor_amount,
    'exp_no':exp_no,
    'exp_amount':exp_amount,
    'user_name':user_name,
    'stk':stk,
    'prod_form':prod_form,
    'dep_form':dep_form})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def depositor_transactions(request,dep_pk):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    dep_trans = Transaction.objects.filter(depositor_id=dep_pk)
    dep = get_object_or_404(Depositor,pk=dep_pk)
    depname = dep.fname + ' ' + dep.lname
    val_set = ''
    total_amt = 0
    total_dep = 0
    total_wit = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'Transactions for {depname} from {start} to {end}'
        dep_trans = Transaction.objects.filter(depositor_id=dep_pk,date__date__lte=end,date__date__gte=start)
        for trans in dep_trans:
            total_amt += 1
            if trans.action == 'Withdraw':
                total_wit += trans.amount
            elif trans.action == 'Deposit':
                total_dep += trans.amount
    return render(request, 'admin/depositor_transactions.html', {'val_set':val_set,'total_amt':total_amt,'total_dep':total_dep,'total_wit':total_wit,'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'dep_trans': dep_trans,'dep': dep})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def view_creditors(request):
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    credit_list = Sale.objects.all() 
    val_set = ''
    # total_amount = 0
    # total_price = 0
    # sale_no = 0
    if request.method == 'POST': 
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        credit_list = Sale.objects.filter(date__date__lte=end,date__date__gte=start)
        # for sale in credit_list :
        #     total_price += sale.total_price
        #     total_amount += sale.total_amount_paid
        # sale_no = credit_list .count()
    return render(request, 'admin/view_creditors.html', {'user_name':user_name,'stk':stk,'prod_form':prod_form,'dep_form':dep_form,'credit_list': credit_list})

#mobile
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_mobile_sales(request):
    user_name = request.user.sup_user
    mob_sales= Sale.objects.filter(seller__type='mob')
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    if request.method == 'POST': 
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        mob_sales= Sale.objects.filter(date__date__lte=end,date__date__gte=start)
        for sale in mob_sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
        sale_no = mob_sales.count()
    return render(request, 'admin/admin_view_mobile_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'mob_sales':mob_sales,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_mobile_payment(request,sid):
    user_name = request.user.sup_user
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'admin/admin_mobile_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_mobile_payment(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.sup_user
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_mobile_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/admin_view_mobile_payment/{sid}/')
    return render(request, 'admin/admin_mobile_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_mobile_sale_product(request,sid):
    user_name = request.user.sup_user
    mob_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'admin/admin_view_mobile_sale_products.html',{'mob_sales_prod':mob_sales_prod,'user_name':user_name,'title': 'Home'})



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_mobile_reciept(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.sup_user
    mob_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'admin/admin_mobile_reciept.html', {'amount_paid':amount_paid,'mob_sale':mob_sale,'payment':payment,'balance':balance, 'total_price':total_price, 'user_name':user_name,'title': 'Print Invoice'})

#electroics
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_electronic_sales(request):
    user_name = request.user.sup_user
    ele_sales= Sale.objects.filter(seller__type='ele')
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    if request.method == 'POST': 
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        ele_sales= Sale.objects.filter(seller__type='ele',date__date__lte=end,date__date__gte=start)
        for sale in ele_sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
        sale_no = ele_sales.count()
    return render(request, 'admin/admin_view_electronic_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'ele_sales':ele_sales,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_electronics_sale_product(request,sid):
    user_name = request.user.sup_user
    ele_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'admin/admin_electronics_sale_products.html', {'ele_sales_prod':ele_sales_prod,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_electronic_payment(request,sid):
    user_name = request.user.sup_user
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'admin/admin_electronic_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments, 'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_electronic_payment(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.sup_user
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_electronic_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/admin_view_electronic_payment/{sid}/')
    return render(request, 'admin/admin_electronic_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_electronic_reciept(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.sup_user
    ele_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'admin/admin_electronics_reciept.html', {'amount_paid':amount_paid,'ele_sale':ele_sale,'payment':payment,'balance':balance, 'total_price':total_price, 'user_name':user_name,'title': 'Print Invoice'})

#accessories
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_accessories_sales(request):
    user_name = request.user.sup_user
    acc_sales= Sale.objects.filter(seller__type='acc')
    val_set = ''
    total_amount = 0
    total_price = 0
    sale_no = 0
    if request.method == 'POST':
        start = request.POST['startdate']
        end = request.POST['enddate']
        val_set = f'All Sales from {start} to {end}'
        acc_sales = Sale.objects.filter(seller= user_name,date__date__lte=end,date__date__gte=start)
        for sale in acc_sales:
            total_price += sale.total_price
            total_amount += sale.total_amount_paid
        sale_no = acc_sales.count()
    return render(request, 'admin/admin_view_accessories_sales.html', {'sale_no':sale_no,'total_amount':total_amount,'total_price':total_price,'val_set':val_set,'acc_sales':acc_sales,'user_name':user_name,'title': 'View Sales'})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_accessories_sale_product(request,sid):
    user_name = request.user.sup_user
    acc_sales_prod = Product_Group.objects.filter(sale__id=sid)
    return render(request, 'admin/admin_accessories_sale_products.html', {'acc_sales_prod':acc_sales_prod,'user_name':user_name,'title': 'Home'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_view_accessories_payment(request,sid):
    user_name = request.user.sup_user
    payments = Payment.objects.filter(sale__id=sid)
    sale = get_object_or_404(Sale,pk=sid)
    bal = sale.total_price-sale.total_amount_paid
    return render(request, 'admin/admin_accessories_sale_payment.html', {'bal':bal,'sid':sid,'payments': payments,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_accessories_payment(request,sid):
    pay_form = AddPayment()
    acc_form = SaleForm()
    user_name = request.user.sup_user
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formTwenty':
            acc_form = SaleForm(request.POST)
            if acc_form.is_valid():
                name = acc_form.cleaned_data['cust_name']
                address = acc_form.cleaned_data['cust_address']
                telephone = acc_form.cleaned_data['cust_tel']
                total_amount_paid = acc_form.cleaned_data['total_amount_paid']
                quantity = acc_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/view_accessories_sales/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentyone':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/admin_view_accessories_payment/{sid}/')
    return render(request, 'admin/admin_accessories_add_payment.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'acc_form':acc_form,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_accessories_reciept(request,pid):
    user_name = request.user
    payment = get_object_or_404(Payment,pk=pid)
    total_price = payment.sale.total_price
    amount_paid = payment.total_amount
    balance = total_balance(total_price,payment.sale.total_amount_paid)
    user_name = request.user.sup_user
    acc_sale = Product_Group.objects.filter(sale__id=payment.sale.id)
    return render(request, 'admin/admin_accessories_reciept.html', {'amount_paid':amount_paid,'acc_sale':acc_sale,'payment':payment,'balance':balance, 'total_price':total_price,'user_name':user_name,'title': 'Print Invoice'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_receipt(request,rid):
    obj = get_object_or_404(Receipt,pk=rid)
    rec_form = ReceiptUpdateForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
            rec_form = ReceiptUpdateForm(request.POST,request.FILES, instance=obj)
            if rec_form.is_valid():
                rec_form.save()
                messages.success(request, 'Success!! Staff updated sucessfully')
                return redirect('/admin_view_receipt/')
    return render(request, 'admin/edit_receipt.html',{'user_name':user_name,'stk':stk,'rec_form':rec_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_invoice(request,iid):
    obj = get_object_or_404(Invoice,pk=iid)
    inv_form = InvoiceUpdateForm(instance=obj)
    stk = Stock.objects.filter(quantity=0)
    dep_form = DepositorForm()
    prod_form = ProductForm()
    user_name = request.user.sup_user
    if request.method == 'POST':
            inv_form = InvoiceUpdateForm(request.POST,request.FILES, instance=obj)
            if inv_form.is_valid():
                inv_form.save()
                messages.success(request, 'Success!! Invoice updated sucessfully')
                return redirect('/admin_view_invoice/')
    return render(request, 'admin/edit_invoice.html',{'user_name':user_name,'stk':stk,'inv_form':inv_form,'prod_form':prod_form,'dep_form':dep_form})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_edit_mobile_sale(request,sid):
    user_name = request.user.sup_user
    sal = get_object_or_404(Sale,pk=sid)
    mob_form = UpdateSaleForm(instance=sal)
    if request.method == 'POST':
        mob_form = UpdateSaleForm(request.POST,instance=sal)
        if mob_form.is_valid():
            mob_form.save()
            messages.success(request, 'Success!! Customer details updated sucessfully')
            return redirect('/admin_view_mobile_sales/')
        else:
            messages.warning(request, 'Error!! Could not Update')
    return render(request, 'admin/edit_mobile_sale.html', {'mob_form':mob_form,'user_name':user_name,'title': 'View Sales'})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin_add_payments(request,sid):
    pay_form = AddPayment()
    mob_form = SaleForm()
    user_name = request.user.sup_user
    products = Stock.objects.filter(seller__id=user_name.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formEighteen':
            mob_form = SaleForm(request.POST)
            if mob_form.is_valid():
                name = mob_form.cleaned_data['cust_name']
                address = mob_form.cleaned_data['cust_address']
                telephone = mob_form.cleaned_data['cust_tel']
                total_amount_paid = mob_form.cleaned_data['total_amount_paid']
                quantity = mob_form.cleaned_data['quantity']
                product_id = request.POST['prod']
                product = get_object_or_404(Product,pk=product_id)
                total_price = product.price * quantity
                tar_prod = Stock.objects.get(seller__id=user_name.id,product__id=product_id)
                bal = total_price - total_amount_paid
                if int(total_amount_paid) >= 0:
                    if int(quantity) > 0:
                        if quantity <= tar_prod.quantity:
                            if bal < 0:
                                messages.warning(request, '!!!ERROR!!! The amount paid is more than the total price.')
                            else:
                                tar_prod.quantity = F('quantity') - quantity
                                tar_prod.save()
                                sale = Sale.objects.create(product=product,seller=user_name,quantity=quantity,total_price=total_price,total_amount_paid=total_amount_paid,cust_name=name,cust_tel=telephone,cust_address=address)
                                Payment.objects.create(sale=sale,amount=total_amount_paid,total_amount=total_amount_paid,balance=bal,date=timezone.now())
                                acc = Account.objects.all()[0]
                                acc.balance += int(total_amount_paid)
                                acc.save()
                                messages.success(request, 'Success!! Sale made sucessfully')
                                return redirect('/admin_home/')
                        else:
                            messages.warning(request, f"!!!ERROR!!! You only have {tar_prod.quantity} {product.name} products in your inventory")
                    else:
                        messages.warning(request, "!!!ERROR!!! Your quantity should be more than zero")    
                else:
                    messages.warning(request, "!!!ERROR!!! Your payment amount cannot be negetive")
        elif request.POST.get("form_type") == 'formTwentythree':
            pay_form = AddPayment(request.POST)
            if pay_form.is_valid():
                amount = pay_form.cleaned_data['amount']
                descp = request.POST['desc']
                sale = get_object_or_404(Sale,pk=sid)
                total_amt = sale.total_amount_paid + amount
                bal = sale.total_price - total_amt
                val = sale.total_price - sale.total_amount_paid
                if amount>val:
                    messages.warning(request, 'Error!! Amount paid more than balance')
                else:
                    if descp:
                        Payment.objects.create(sale=sale,amount=amount,desc=descp,total_amount=total_amt,balance=bal,date=timezone.now())
                    else:
                        Payment.objects.create(sale=sale,amount=amount,total_amount=total_amt,balance=bal,date=timezone.now())
                    sale.total_amount_paid += amount
                    sale.save()
                    acc = Account.objects.all()[0]
                    acc.balance += amount
                    acc.save()
                    messages.success(request, 'Success!! Payment made sucessfully')
                    return redirect(f'/admin_sale_payments/{sid}/')
    return render(request, 'admin/admin_add_payments.html', {'sid':sid,'pay_form':pay_form,'products':products,'user_name':user_name,'mob_form':mob_form,'title': 'View Sales'})
