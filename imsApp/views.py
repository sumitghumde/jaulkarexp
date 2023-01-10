from email import message

from django.db.migrations import serializer
from django.template.loader import get_template
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from ims_django.settings import MEDIA_ROOT, MEDIA_URL
from django.core import serializers
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from imsApp.forms import *  # SaveStock, UserRegistration, UpdateProfile, UpdatePasswords, SaveCategory, SaveProduct, SaveInvoice, SaveInvoiceItem
from imsApp.models import *  # Category, Product, Stock, Invoice, Invoice_Item
# from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

context = {
    'page_title': 'File Management System',
}
dataget = {}


# login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    context['page_title'] = 'Home'
    context['drivers'] = Driver.objects.count()
    context['helpers'] = Helper.objects.count()
    context['customers'] = Customer.objects.count()
    context['tractors'] = Tractor.objects.count()
    context['items'] = Item.objects.count()
    context['invoices'] = Invoice.objects.count()
    return render(request, 'home.html', context)


def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username=username, password=pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request, 'register.html', context)


@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id=request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        # print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form

    return render(request, 'manage_profile.html', context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html', context)


# Driver
# Create by Sumit Ghumde 27 Oct 2022

@login_required
def driver_mgt(request):
    context['page_title'] = "Driver"
    drivers = Driver.objects.all()
    context['drivers'] = drivers

    return render(request, 'driver_mgt.html', context)


@login_required
def save_driver(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            drivers = Driver.objects.get(pk=request.POST['id'])
        else:
            drivers = None
        if drivers is None:
            form = SaveDriver(request.POST)
        else:
            form = SaveDriver(request.POST, instance=drivers)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_driver(request, pk=None):
    context['page_title'] = "Manage Driver"
    if not pk is None:
        drivers = Driver.objects.get(id=pk)
        context['drivers'] = drivers
    else:
        context['drivers'] = {}

    return render(request, 'manage_driver.html', context)


def sales_injson(drivers, helpers, customers, invoice_items, invoices, pk):
    return {
        'drivers': serializers.serialize("json", drivers),
        'helpers': serializers.serialize("json", helpers),
        'customers': serializers.serialize("json", customers),
        'invoiceitems': serializers.serialize("json", invoice_items),
        'invoices': serializers.serialize("json", invoices),
        'invid': pk
    }
    # return json_context


@login_required
def manage_sales(request, pk=None):
    # context['page_title'] = "Manage Driver"
    context['page_title'] = 'Edit Sales'
    invoice_items = Invoice_Item.objects.filter(invoice_id=pk).all()
    invoices = Invoice.objects.filter(id=pk)
    drivers = Driver.objects.all()
    customers = Customer.objects.all()
    helpers = Helper.objects.all()
    context['drivers'] = drivers
    # # printt(type(drivers))
    context['helpers'] = helpers
    context['customers'] = customers
    context['invoiceitems'] = invoice_items
    context['invoices'] = invoices
    context['invid'] = pk
    # context['serialized_data'] = json.dumps(context)
    dataget['thingy_json'] = context
    # printt("++++|||||||||||||||||||||||||||+++++++++++++++++++++")
    # printt(type(context))
    json_context = json.dumps(serializer.sales_injson(drivers, helpers, customers, invoice_items, invoices, pk))
    # loaded_r = json.loads(json_context)
    json_object = json.loads(json_context)
    # printt(json_context)
    # for i in json_context:
        # printt(type(i))
    # printt(type(json_object))
    # context['diesel'] = invoices.diesel
    # printt("++++++++++++++++++++Hello context++++++++++++++++++++++")
    # resp['status'] = 'success'
    return render(request, 'salesedit.html', json_object)

    # return render(request, 'salesedit.html', context)


@login_required
def delete_driver(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            # printt("driver++")
            # printt(request.POST['id'])
            driveruse = Invoice.objects.get(driver_id=request.POST['id'])
            # printt(driveruse, "hello")
            if driveruse[0][0] == None:
                drivers = Driver.objects.get(id=request.POST['id'])
                drivers.delete()
                messages.success(request, 'Driver has been deleted successfully')
                resp['status'] = 'success'
            else:
                # # printt("driver++")
                resp['msg'] = 'Driver has failed to delete'
        except Exception as err:
            # printt("driver++")
            resp['msg'] = 'Driver has failed to delete'
            # printt(err)
    else:
        resp['msg'] = 'Driver has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


# Category
@login_required
def category_mgt(request):
    context['page_title'] = "Item Categories"
    categories = Category.objects.all()
    context['categories'] = categories
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)

    return render(request, 'category_mgt.html', context)


@login_required
def save_category(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            category = Category.objects.get(pk=request.POST['id'])
        else:
            category = None
        if category is None:
            form = SaveCategory(request.POST)
        else:
            form = SaveCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_category(request, pk=None):
    context['page_title'] = "Manage Category"
    if not pk is None:
        category = Category.objects.get(id=pk)
        context['category'] = category
    else:
        context['category'] = {}

    return render(request, 'manage_category.html', context)


@login_required
def delete_category(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            category = Category.objects.get(id=request.POST['id'])
            category.delete()
            messages.success(request, 'Category has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Category has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Category has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


# product
@login_required
def product_mgt(request):
    context['page_title'] = "Product List"
    products = Product.objects.all()
    context['products'] = products

    return render(request, 'product_mgt.html', context)


@login_required
def save_product(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            product = Product.objects.get(pk=request.POST['id'])
        else:
            product = None
        if product is None:
            form = SaveProduct(request.POST)
        else:
            form = SaveProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_product(request, pk=None):
    context['page_title'] = "Manage Product"
    if not pk is None:
        product = Product.objects.get(id=pk)
        context['product'] = product
    else:
        context['product'] = {}

    return render(request, 'manage_product.html', context)


@login_required
def delete_product(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            product = Product.objects.get(id=request.POST['id'])
            product.delete()
            messages.success(request, 'Product has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Product has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Product has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


# Customer
@login_required
def customer_mgt(request):
    context['page_title'] = "Customer"
    customers = Customer.objects.all()
    context['customers'] = customers
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)

    return render(request, 'customer_mgt.html', context)


@login_required
def save_customer(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            customer = Customer.objects.get(pk=request.POST['id'])
        else:
            customer = None
        if customer is None:
            form = SaveCustomer(request.POST)
        else:
            form = SaveCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_customer(request, pk=None):
    context['page_title'] = "Manage Customer"
    if not pk is None:
        customer = Customer.objects.get(id=pk)
        context['customers'] = customer
    else:
        context['customers'] = {}

    return render(request, 'manage_customer.html', context)


@login_required
def delete_customer(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=request.POST['id'])
            customer.delete()
            messages.success(request, 'customer has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'customer has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Category has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


# Helper

@login_required
def helper_mgt(request):
    context['page_title'] = "Helper"
    helpers = Helper.objects.all()
    context['helpers'] = helpers
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)

    return render(request, 'helper_mgt.html', context)


@login_required
def save_helper(request):
    # printt("Fiwerst +++++++++++++++++++++++")
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            helpers = Helper.objects.get(pk=request.POST['id'])
        else:
            helpers = None
        if helpers is None:
            form = SaveHelper(request.POST)
        else:
            form = SaveHelper(request.POST, instance=helpers)
        if form.is_valid():
            form.save()
            messages.success(request, 'Helper has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_helper(request, pk=None):
    context['page_title'] = "Manage Customer"
    if not pk is None:
        helper = Helper.objects.get(id=pk)
        context['helpers'] = helper
    else:
        context['helpers'] = {}

    return render(request, 'manage_helper.html', context)


@login_required
def delete_helper(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            helper = Helper.objects.get(id=request.POST['id'])
            helper.delete()
            messages.success(request, 'Helper has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Helper has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Helper has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


# Inventory
@login_required
def inventory(request):
    context['page_title'] = 'Inventory'

    products = Product.objects.all()
    context['products'] = products

    return render(request, 'inventory.html', context)


# Inventory History
@login_required
def inv_history(request, pk=None):
    context['page_title'] = 'Inventory History'
    if pk is None:
        messages.error(request, "Product ID is not recognized")
        return redirect('inventory-page')
    else:
        product = Product.objects.get(id=pk)
        stocks = Stock.objects.filter(product=product).all()
        context['product'] = product
        context['stocks'] = stocks

        return render(request, 'inventory-history.html', context)


# Stock Form
@login_required
def manage_stock(request, pid=None, pk=None):
    if pid is None:
        messages.error(request, "Product ID is not recognized")
        return redirect('inventory-page')
    context['pid'] = pid
    if pk is None:
        context['page_title'] = "Add New Stock"
        context['stock'] = {}
    else:
        context['page_title'] = "Manage New Stock"
        stock = Stock.objects.get(id=pk)
        context['stock'] = stock

    return render(request, 'manage_stock.html', context)


@login_required
def save_stock(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            stock = Stock.objects.get(pk=request.POST['id'])
        else:
            stock = None
        if stock is None:
            form = SaveStock(request.POST)
        else:
            form = SaveStock(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def delete_stock(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            stock = Stock.objects.get(id=request.POST['id'])
            stock.delete()
            messages.success(request, 'Stock has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Stock has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Stock has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def sales_mgt(request):
    context['page_title'] = 'Sales'
    products = Product.objects.filter(status=1).all()
    drivers = Driver.objects.all()
    customers = Customer.objects.all()
    tractors = Tractor.objects.all()
    site = Site.objects.all()
    totaled = Item.objects.values_list('totalstock').filter(itemname='ED')
    totalgl = Item.objects.values_list('totalstock').filter(itemname='GL')
    totalnonel = Item.objects.values_list('totalstock').filter(itemname='NONEL')
    totaldf = Item.objects.values_list('totalstock').filter(itemname='DF')
    # printt(tractors)
    helpers = Helper.objects.all()
    context['products'] = products
    context['drivers'] = drivers
    context['helpers'] = helpers
    context['customers'] = customers
    context['tractors'] = tractors
    context['sites'] = site
    context['totaleds'] = totaled[0][0]
    # printt(totaled, "+++++++++++++++++++++++++++rd++++++++++++++++++++")
    context['totalgls'] = totalgl[0][0]
    context['totalnonels'] = totalnonel[0][0]
    context['totaldf'] = totaldf[0][0]

    return render(request, 'sales.html', context)


def get_product(request, pk=None, sid=None):
    resp = {'status': 'failed', 'data': {}, 'msg': ''}
    if pk is None:
        resp['msg'] = 'Customer ID is not recognized'
    else:
        customer = Customer.objects.get(id=pk)
        resp['data']['customer'] = str(str(customer.id) + " - " + customer.name)
        resp['data']['id'] = customer.id
        site = Site.objects.get(id=sid)
        resp['data']['site'] = str(str(site.id) + " - " + site.sitename)
        resp['data']['sid'] = site.id
        # resp['data']['price'] = driver.price
        resp['status'] = 'success'

    return HttpResponse(json.dumps(resp), content_type="application/json")


def update_before_deletestock(data):
    # printt("+++++++++++++++++++show ed +++++++++++++++++++")
    edgl = Invoice.objects.values_list('ed', 'gl').filter(id=data['id'])
    # printt(edgl)
    gl = Invoice.objects.values_list('gl').filter(id=data['id'])
    totaled = Item.objects.values_list('totalstock').filter(itemname='ED')
    totalgl = Item.objects.values_list('totalstock').filter(itemname='GL')
    ed = (list(edgl)[0][0])
    gl = (list(edgl)[0][1])
    # printt(ed)
    # printt(gl)
    # printt(totaled[0][0])
    # printt(totalgl[0][0])
    totaled = int(totaled[0][0]) + int(ed)
    totalgl = int(totalgl[0][0]) + int(gl)
    # printt(totaled, " ::-----::", totalgl)
    Item.objects.filter(itemname='ED').update(totalstock=totaled)
    Item.objects.filter(itemname='GL').update(totalstock=totalgl)

    # Invoice_Item.objects.filter(id=instance.id).update(stock=stock)


def update_stock(data):
    ed = data['ed']
    gl = data['gl']
    nonel = data['nonel']
    df = data['df']
    totaled = Item.objects.values_list('totalstock').filter(itemname='ED')
    totalnonel = Item.objects.values_list('totalstock').filter(itemname='NONEL')
    totaldf = Item.objects.values_list('totalstock').filter(itemname='DF')

    # # printt(totaled[0])
    # x=totaled[0]
    # # printt(x[0])
    totalgl = Item.objects.values_list('totalstock').filter(itemname='GL')
    # # printt(totalgl[0])
    totaled = int(totaled[0][0]) - int(ed)
    totalgl = int(totalgl[0][0]) - int(gl)
    totalnonel = int(totalnonel[0][0]) - int(nonel)
    totaldf = int(totaldf[0][0]) - int(df)
    # printt(totaled, " ::-----::", totalgl)
    Item.objects.filter(itemname='ED').update(totalstock=totaled)
    Item.objects.filter(itemname='GL').update(totalstock=totalgl)
    Item.objects.filter(itemname='NONEL').update(totalstock=totalnonel)
    Item.objects.filter(itemname='DF').update(totalstock=totaldf)

    # Invoice_Item.objects.filter(id=instance.id).update(stock=stock)


def save_sales(request):
    # printt("++++++++++++++++++++++++hello+++++++++++++++++++")
    resp = {'status': 'failed', 'msg': ''}
    # id = 2
    if request.method == 'POST':
        # datareq = request.POST
        # # printt(datareq['ed'])
        # printt("++++++++++++++++++++++++hello1+++++++++++++++++++")
        cids = request.POST.getlist('cid[]')
        sids = request.POST.getlist('sid[]')
        # printt(len(cids), "+++++++++++++++++++++++++++44444444444444444")
        if len(cids) > 0:
            # printt(cids)
            # printt(sids)
            cnt = 0
            invoice_form = SaveInvoice(request.POST)
            # printt("++++++++++++++++++++++++hello2+++++++++++++++++++")
            # # printt(invoice_form.is_valid())
            if invoice_form.is_valid():
                # printt("++++++++++++++++++++++++hello3+++++++++++++++++++")
                invoice_form.save()
                update_stock(request.POST)
                invoice = Invoice.objects.last()
                # printt(request.POST)
                # printt("++++++++++++++++++++++++hello4+++++++++++++++++++")
                # printt(cids)
                for cid in cids:
                    # # printt( int(request.POST['sid[' + str(sids[cnt]) + ']']))
                    # printt("customer id :--", cid)
                    qty25 = int(request.POST['thussi[' + str(cid) + ']']) + int(
                        request.POST['hole25[' + str(cid) + ']']) + (
                                    int(request.POST['hole5[' + str(cid) + ']']) * 2)
                    totalamtcust = qty25 * int(request.POST['amount[' + str(cid) + ']'])
                    datareceipt = {
                        'invoice': invoice.id,
                        'customer': int(cid),
                        'site': sids[cnt],
                        'total': totalamtcust,
                        'deposit': request.POST['deposit[' + str(cid) + ']'],
                        'balance': str((int(qty25) * int(request.POST['amount[' + str(cid) + ']'])) - int(
                            request.POST['deposit[' + str(cid) + ']']))
                    }
                    data = {
                        'invoice': invoice.id,
                        'customer': int(cid),
                        'hole25': request.POST['hole25[' + str(cid) + ']'],
                        'hole5': request.POST['hole5[' + str(cid) + ']'],
                        'thussi': request.POST['thussi[' + str(cid) + ']'],
                        'price': request.POST['amount[' + str(cid) + ']'],
                        'total': totalamtcust,
                        'deposit': request.POST['deposit[' + str(cid) + ']'],
                        # 'balance': request.POST['balance[' + str(cid) + ']'],
                        'site': sids[cnt],
                        # # 'product': cid,
                        'quantity': str(qty25),
                        'balance': str((int(qty25) * int(request.POST['amount[' + str(cid) + ']'])) - int(
                            request.POST['deposit[' + str(cid) + ']']))
                    }
                    # printt("++++++++++++++++++++45464555454 hello 5666622377363+++++++++++++++++++++++")
                    # printt(data)
                    # printt(type(data['site']))
                    ii_form = SaveInvoiceItem(data=data)
                    # printt("++++++++++++++++++++hello5+++++++++++++++++++++++")
                    # printt(ii_form.data)
                    # printt("++++++++++++++++++++hello6+++++++++++++++++++++++")
                    # printt(ii_form.is_valid())
                    if ii_form.is_valid():
                        ii_form.save()
                        receipt_form = SaveReceiptinvoice(data=datareceipt)
                        if receipt_form.is_valid():
                            receipt_form.save()
                        # else:
                            # printt('+++++++++++++++++++++HelloFalse Data Got++++++++++++++++++++')
                        cnt = cnt + 1
                    else:
                        # printt('+++++++++++++++++++++Hello7++++++++++++++++++++')
                        # for i in invoice_form:
                            # printt("Error:", i, i.errors)
                        # printt('+++++++++++++++++++++Hello8++++++++++++++++++++')
                        for fields in ii_form:
                            for error in fields.errors:
                                resp['msg'] += str(error + "<br>")
                        break
                messages.success(request, "Sale Transaction has been saved.")
                resp['status'] = 'success'
                # invoice.delete()
            # else:
                # for i in invoice_form:
                    # printt("Error:", i, i.errors)
                # for fields in invoice_form:
                #     for error in fields.errors:
                #         # printt(str(error))
                #         resp['msg'] += str(error + "<br>")
                #         # printt(resp['msg'])

    return HttpResponse(json.dumps(resp), content_type="application/json")


# def save_sales(request):
#     resp = {'status':'failed', 'msg' : ''}
#     id = 2
#     if request.method == 'POST':
#         pids = request.POST.getlist('pid[]')
#         invoice_form = SaveInvoice(request.POST)
#         if invoice_form.is_valid():
#             invoice_form.save()
#             invoice = Invoice.objects.last()
#             for pid in pids:
#                 data = {
#                     'invoice':invoice.id,
#                     'product':pid,
#                     'quantity':request.POST['quantity['+str(pid)+']'],
#                     'price':request.POST['price['+str(pid)+']'],
#                 }
#                 # printt(data)
#                 ii_form = SaveInvoiceItem(data=data)
#                 # # printt(ii_form.data)
#                 if ii_form.is_valid():
#                     ii_form.save()
#                 else:
#                     for fields in ii_form:
#                         for error in fields.errors:
#                             resp['msg'] += str(error + "<br>")
#                     break
#             messages.success(request, "Sale Transaction has been saved.")
#             resp['status'] = 'success'
#             # invoice.delete()
#         else:
#             for fields in invoice_form:
#                 for error in fields.errors:
#                     resp['msg'] += str(error + "<br>")
#
#     return HttpResponse(json.dumps(resp),content_type="application/json")
def columndata(tablename, dataid, columnname, query):
    import sqlite3

    # Connecting to sqlite
    conn = sqlite3.connect('db.sqlite3')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    sqlquery = ""
    if query == "":
        sqlquery = "select " + str(columnname) + " from " + str(tablename) + " where id = " + str(dataid)
    else:
        sqlquery = query
    # printt(sqlquery)
    x = cursor.execute(str(sqlquery))
    # printt("+++++++Cursor data+++++++++++++++++")
    # printt(type(x))
    # printt(x)
    if query == "":
        # Fetching 1st row from the table
        result = cursor.fetchone();
        # printt("+++++++Cursor data1+++++++++++++++++")
        # printt(result)
        return result
    else:
        # Fetching 1st row from the table
        result = cursor.fetchall();
        # printt("+++++++Cursor data All+++++++++++++++++")
        # printt(type(result))
        return result


@login_required
def invoices(request):
    invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    context['invoices'] = invoice
    dataquery = """SELECT *
FROM imsApp_invoice
JOIN imsApp_driver
  ON imsApp_invoice.driver_id = imsApp_driver.id
JOIN imsApp_helper
  ON imsApp_invoice.helper_id = imsApp_helper.id;"""
    context['invoices'] = columndata("", "", "", dataquery)
    return render(request, 'invoices.html', context)


@login_required
def delete_invoice(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            data = request.POST
            update_before_deletestock(data)
            invoice = Invoice.objects.get(id=request.POST['id'])
            invoice.delete()
            messages.success(request, 'Invoice has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Invoice has failed to delete'
            # printt(err)

    else:
        resp['msg'] = 'Invoice has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def edit_invoice(request):
    resp = {'status': 'failed', 'msg': ''}
    # printt("+++++++++++++context # printt 0 f++++++++++++++++++")

    # if request.method == 'POST':
    try:
        # invoice = Invoice.objects.filter(id=request.POST['id']).all()
        context['page_title'] = 'Edit Sales'
        invoice_items = Invoice_Item.objects.filter(invoice_id=102).all()
        invoices = Invoice.objects.filter(id=102)
        drivers = Driver.objects.all()
        customers = Customer.objects.all()
        helpers = Helper.objects.all()
        context['drivers'] = drivers
        context['helpers'] = helpers
        context['customers'] = customers
        context['invoiceitems'] = invoice_items
        context['invoices'] = invoices
        # printt("++++++++++++++++++++Hello context++++++++++++++++++++++")
        resp['status'] = 'success'
        return render(request, 'salesedit.html', context)

    except Exception as err:
        resp['msg'] = 'Invoice has failed to delete'
        # printt(err)


# ------------------------ PDF Page Code -------------------------------------------
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def invoicespdf(request):
    invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    context['invoices'] = invoice
    dataquery = """SELECT inv.id,drv.name,hlp.helpername,cust.name,inv.ed,inv.gl,inv.nonel,strftime('%d/%m/%Y',DATE(inv.date_created)) as date_created,inv.diesel,
invitem.hole25,invitem.hole5,invitem.price, ((invitem.thussi+invitem.hole25+(invitem.hole5 *2))*invitem.price) as total, invitem.deposit,invitem.balance,invitem.quantity,invitem.thussi,inv.df
FROM imsApp_invoice as inv
JOIN imsApp_driver as drv
  ON inv.driver_id = drv.id
JOIN imsApp_helper as hlp
  ON inv.helper_id = hlp.id
  JOIN imsApp_invoice_item as invitem
  ON inv.id = invitem.invoice_id
  JOIN imsApp_customer as cust
  ON cust.id = invitem.customer_id;"""
    context['invoices'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('invoicespdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def invoicescustomerpdf(request, pk):
    # invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    # context['invoices'] = invoice
    dataquery = """SELECT inv.id,sitename,drv.name,hlp.helpername,cust.name,inv.ed,inv.gl,inv.nonel,strftime('%d/%m/%Y',DATE(inv.date_created)) as date_created,inv.diesel,
invitem.hole25,invitem.hole5,invitem.price, ((invitem.thussi+invitem.hole25+(invitem.hole5 *2))*invitem.price) as total, invitem.deposit,invitem.balance,invitem.quantity,invitem.hole25,invitem.thussi,inv.df,
FROM imsApp_invoice as inv
JOIN imsApp_driver as drv
  ON inv.driver_id = drv.id
JOIN imsApp_helper as hlp
  ON inv.helper_id = hlp.id
  JOIN imsApp_invoice_item as invitem
  ON inv.id = invitem.invoice_id 
  JOIN imsApp_customer as cust
  ON cust.id = invitem.customer_id 
  JOIN imsApp_site as sit
  ON sit.id = invitem.site_id where inv.id = """ + str(pk) + """;"""
    context['invoices'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('invoicespdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def driverpdf(request):
    driver = Driver.objects.all()
    # printt(driver)
    context['page_title'] = 'Drivers'
    context['drivers'] = driver
    dataquery = """SELECT *
    FROM imsApp_driver;"""
    context['drivers'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('driverpdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def helperpdf(request):
    helper = Helper.objects.all()
    # printt(helper)
    context['page_title'] = 'Helpers'
    context['helpers'] = helper
    dataquery = """SELECT *
    FROM imsApp_helper;"""
    context['helpers'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('helperspdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def tractorpdf(request):
    tractor = Tractor.objects.all()
    # printt(tractor)
    context['page_title'] = 'Tractors'
    context['tractors'] = tractor
    dataquery = """SELECT *
        FROM imsApp_tractor;"""
    context['tractors'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('tractorpdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def customerpdf(request):
    customer = Customer.objects.all()
    # printt(customer)
    context['page_title'] = 'Customers'
    context['customers'] = customer
    dataquery = """SELECT *
        FROM imsApp_customer;"""
    context['customers'] = columndata("", "", "", dataquery)
    pdf = render_to_pdf('customerspdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def allpdf(request):
    context['page_title'] = 'Report'
    return render(request, 'allpdf.html', context)
    # else:
    #     resp['msg'] = 'Invoice has failed to delete'

    # return HttpResponse(json.dumps(resp), content_type="application/json")


def customerallbill(request, pk):
    # invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    # sumofamount = """  SELECT sum(invitem.total), sum(invitem.deposit),sum(invitem.balance)
    #   FROM imsApp_invoice as inv
    # JOIN imsApp_receiptinvoice as invitem
    # ON inv.id = invitem.invoice_id
    # JOIN imsApp_customer as cust
    # ON cust.id = invitem.customer_id
    # where cust.id = """ + str(pk) + """;"""
    # context['totals'] = columndata("", "", "", sumofamount)

    dataquery = """  select sum(total) from imsApp_invoice_item 
        where customer_id = """ + str(pk) + """;"""
    context['totamount'] = columndata("", "", "", dataquery)
    # # printt("!!!!!!!!!!!!!!!!!!!!!!Data Totals+++++++++++++++++")
    # # printt(context['totalsamt'][0][0])
    context['totamount'] = 0 if context['totamount'][0][0] == None else context['totamount'][0][0]

    dataquery = """  select sum(deposit) from imsApp_receiptinvoice 
            where customer_id = """ + str(pk) + """;"""
    context['totdeposit'] = columndata("", "", "", dataquery)
    context['totdeposit'] = 0 if context['totdeposit'][0][0] == None else context['totdeposit'][0][0]

    totbalance = int(context['totamount']) - int(context['totdeposit'])
    context['totbalance']=totbalance
    cust = """  select name from imsApp_customer 
           where id = """ + str(pk) + """;"""
    context['customersname'] = columndata("", "", "", cust)
    context['customername']=context['customersname'][0][0]
    # # printt(context['customername'])
    # context["totalamount"] = context['totalsamt'][0][0]
    # # printt("++++++++++++++++++++++++Data Totals+++++++++++++++++")
    if context['totamount'] != None:
        dataquery = """SELECT strftime('%d/%m/%Y',DATE(inv.date_created)) as date_created,inv.id,cust.name,
        invitem.hole25,invitem.hole5,invitem.price,sit.sitename,
        ((invitem.thussi+invitem.hole25+(invitem.hole5 *2))*invitem.price) as total, invitem.deposit,invitem.balance,invitem.quantity,invitem.thussi
        FROM imsApp_invoice as inv
      JOIN imsApp_invoice_item as invitem
      ON inv.id = invitem.invoice_id
      JOIN imsApp_customer as cust
      ON cust.id = invitem.customer_id 
      JOIN imsApp_site as sit
      ON sit.id = invitem.site_id
      where cust.id  = """ + str(pk) + """ order by sit.sitename;"""
        context['customers'] = columndata("", "", "", dataquery)
        pdf = render_to_pdf('customerallbillpdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponseRedirect("/customer")


def customerreceiptdetails(request, pk):
    # invoice = Invoice.objects.all()  context['page_title'] = 'Invoices'
    dataquery = """SELECT strftime('%d/%m/%Y',DATE(inv.date_created)) as date_created,inv.id as Invoice_Id,cust.name,
    sum(invitem.hole25) as hole25,sum(invitem.hole5) as hole5,invitem.price, sum(invitem.total) as total, invitem.quantity,cust.id as custid,site.sitename,site.id,cust.id,sum(invitem.thussi) as thussi 
    FROM imsApp_invoice as inv
  JOIN imsApp_invoice_item as invitem
  ON inv.id = invitem.invoice_id
  JOIN imsApp_customer as cust
  ON cust.id = invitem.customer_id
  JOIN imsApp_site as site
  ON site.id = invitem.site_id   
  where cust.id  = """ + str(pk) + """ GROUP BY invitem.site_id ;"""
    # printt("RRRRRRRRRYYYYYYYYYYYTTTTTTTTTTTTTT")
    # printt(dataquery)
    context['customers'] = columndata("", "", "", dataquery)
    # pdf = render_to_pdf('customerallbillpdf.html', context)
    return render(request, 'customerallbill.html', context)


def customerreceipt(request, siteid, custid):
    # invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    dataquery = """SELECT sum(deposit) from imsApp_receiptinvoice as invitem
    where invitem.customer_id   = """ + str(custid) + """ and invitem.site_id = """ + str(siteid) + """ ;"""
    deposites = columndata("", "", "", dataquery)
    context['deposites'] = 0 if deposites[0][0] == None else deposites[0][0]

    # printt("Hello0000000000000000000000000000000000000000000oooo")
    # printt(dataquery)
    dataquery = """select sum(invitem.total) as total 
    From imsApp_invoice_item as invitem where  invitem.customer_id = 
    """ + str(custid) + """ and invitem.site_id = """ + str(siteid) + """ ;"""
    # printt("LLLLLLLLLLLLLLLLLLLLLGGGGGGGGGGGGGGGGGGG")
    # printt(dataquery)
    totamt = columndata("", "", "", dataquery)
    dataquery = """SELECT name from imsApp_customer where id = 
       """ + str(custid) + """;"""
    cust = columndata("", "", "", dataquery)

    dataquery = """SELECT sitename from imsApp_site where id = 
           """ + str(siteid) + """;"""
    site = columndata("", "", "", dataquery)

    context['totals'] = 0 if totamt[0][0] == None else totamt[0][0]
    context['invoices'] = 0 if site[0][0] == None else site[0][0]
    context['customers'] = 0 if cust[0][0] == None else cust[0][0]
    # context['totals'] = totamt[0][0]
    # context['invoices'] = site[0][0]
    # context['customers'] = cust[0][0]
    context['balances'] = int(context['totals']) - int(context['deposites'])
    # pdf = render_to_pdf('customerallbillpdf.html', context)
    return render(request, 'addreceiptentry.html', context)


def savenewreceipt(request):
    if request.method == "POST":
        dataquery = """SELECT id from imsApp_customer where name = '""" + request.POST['customer'].strip() + """';"""
        custid = columndata("", "", "", dataquery)
        # printt(dataquery)
        # printt(custid)
        dataquery = """SELECT id from imsApp_site where sitename = '""" + request.POST['invoice'].strip() + """';"""
        siteid = columndata("", "", "", dataquery)
        # # printt(request.POST['invoice'])
        # # printt(request.POST['customer'])
        datareceipt = {
            'invoice': '157',
            'customer': custid[0][0],
            'site': siteid[0][0],
            'total': request.POST['total'],
            'deposit': request.POST['deposit'],
            'balance': int(request.POST['balance']) - int(request.POST['deposit'])
        }
        form = SaveReceiptinvoice(data=datareceipt)
        # printt('Balanceeeeeeeeeeeeeeeeeeeeeoooooooolllllllll')
        # printt(request.POST['balance'])
        # printt(form.is_valid())
        if form.is_valid():
            form.save()
            return render(request, 'customerallbillpdf.html', {'form': form, 'success': " Data Inserted Successfully!"})
        else:
            return render(request, 'customerallbillpdf.html', {'form': form, 'error': "Insert Correct Value Here!"})
    return render(request, 'customerallbillpdf.html')


#  Tractor


@login_required
def tractor_mgt(request):
    context['page_title'] = "Tractor"
    tractors = Tractor.objects.all()
    context['tractors'] = tractors
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)
    return render(request, 'tractor_mgt.html', context)


@login_required
def save_tractor(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            tractors = Tractor.objects.get(pk=request.POST['id'])
        else:
            tractors = None
        if tractors is None:
            form = SaveTractor(request.POST)
        else:
            form = SaveTractor(request.POST, instance=tractors)
        if form.is_valid():
            form.save()
            messages.success(request, 'tractor has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_tractor(request, pk=None):
    context['page_title'] = "Manage Tractor"
    if not pk is None:
        tractor = Tractor.objects.get(id=pk)
        context['tractors'] = tractor
        # printt("llllllllllllll++++++++++++++++++++++++++++++++++++++")
        # printt(tractor)
    else:
        context['tractors'] = {}
    return render(request, 'manage_tractor.html', context)


@login_required
def delete_tractor(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        try:
            tractor = Tractor.objects.get(id=request.POST['id'])
            tractor.delete()
            messages.success(request, 'tractor has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'tractor has failed to delete'
            # printt(err)
    else:
        resp['msg'] = 'tractor has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")


#  Items

@login_required
def item_mgt(request):
    context['page_title'] = "Item"
    items = Item.objects.all()
    context['items'] = items
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)
    return render(request, 'item_mgt.html', context)


@login_required
def save_item(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            items = Item.objects.get(pk=request.POST['id'])
        else:
            items = None
        if items is None:
            form = SaveItem(request.POST)
        else:
            form = SaveItem(request.POST, instance=items)
        if form.is_valid():
            form.save()
            messages.success(request, 'items has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_item(request, pk=None):
    context['page_title'] = "Manage Item"
    if not pk is None:
        item = Item.objects.get(id=pk)
        context['items'] = item
    else:
        context['items'] = {}
    return render(request, 'manage_item.html', context)


@login_required
def delete_item(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=request.POST['id'])
            item.delete()
            messages.success(request, 'item has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'item has failed to delete'
            # printt(err)
    else:
        resp['msg'] = 'item has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Site


@login_required
def site_mgt(request):
    context['page_title'] = "Site"
    sites = Site.objects.all()
    context['sites'] = sites
    # context['contextjson']=json.loads(context)
    # dataget['thingy_json'] = json.dumps(object.context)
    return render(request, 'site_mgt.html', context)


@login_required
def save_site(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            sites = Site.objects.get(pk=request.POST['id'])
        else:
            sites = None
        if sites is None:
            form = SaveSite(request.POST)
        else:
            form = SaveSite(request.POST, instance=sites)
        if form.is_valid():
            form.save()
            messages.success(request, 'sites has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def manage_site(request, pk=None):
    context['page_title'] = "Manage Item"
    if not pk is None:
        site = Site.objects.get(id=pk)
        context['sites'] = site
    else:
        context['sites'] = {}
    return render(request, 'manage_site.html', context)


@login_required
def delete_site(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        try:
            site = Site.objects.get(id=request.POST['id'])
            site.delete()
            messages.success(request, 'site has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'site has failed to delete'
            # printt(err)
    else:
        resp['msg'] = 'site has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")


def totalusepdf(request, pk=None):
    context['page_title'] = 'Invoices'
    dataquery = """ SELECT drv.name, sum(gl) as gelleting ,sum(ed) as Detonetor,sum(nonel) as nonel, sum(diesel) as diesel ,sum(df) as df 
    FROM imsApp_invoice as inv
    JOIN imsApp_driver as drv
    on inv.driver_id= drv.id WHERE inv.driver_id =  """ + str(pk) + """ ; """
    context['invoices'] = columndata("", "", "", dataquery)
    if context["invoices"][0][0] != None:
        pdf = render_to_pdf('totaluse.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponseRedirect("/driver")


def datewisedriver(request, pk=None):
    drvinoice = Invoice.objects.filter(driver_id=pk)
    context['driverid'] = pk
    context['driverinvoices'] = drvinoice
    # printt(pk)
    resp = {'status': 'failed', 'msg': ''}
    resp['status'] = 'success'
    return render(request, "manage_datewisedriverreport.html", context)


def datewisedriverreport(request, pk=None):
    # invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    # printt(request.POST)
    fromdate = request.POST.get('fromdate')
    # printt("From date NEW***********************invoice******************")
    # printt(fromdate)
    todate = request.POST.get('todate')
    drvid = request.POST.get('drvid')
    dataquery = """ SELECT drv.name, sum(gl) as gelleting ,sum(ed) as Detonetor,sum(nonel) as nonel, sum(diesel) as diesel , sum(df) as df 
    FROM imsApp_invoice as inv
    JOIN imsApp_driver as drv
    on inv.driver_id= drv.id WHERE driver_id =  """ + str(drvid) + """ and inv.date_created between '""" + str(
        fromdate) + """' and '""" + str(todate) + """' ; """
    # printt("NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    # printt(dataquery)

    context['invoices'] = columndata("", "", "", dataquery)
    context['driver'] = context['invoices'][0][0]
    # printt("""""""""""""""""context['invoices']""""""""""""""""")
    context['fromdate'] = fromdate
    context['todate'] = todate
    if context["invoices"][0][0] != None:
        pdf = render_to_pdf('driver_totaluse_datewise.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponseRedirect("/driver")


def datewisecustomer(request, pk=None):
    custinoice = Invoice_Item.objects.filter(customer_id=pk)
    context['customerid'] = pk
    context['custinvoices'] = custinoice
    # printt(pk)
    resp = {'status': 'failed', 'msg': ''}
    resp['status'] = 'success'
    return render(request, "manage_customerreport.html", context)
def datewisecustomersitewise(request, pk=None):
    custinoice = Invoice_Item.objects.filter(customer_id=pk)
    context['customerid'] = pk
    context['custinvoices'] = custinoice
    dataquery = """ SELECT distinct(site.sitename),site.id from imsApp_invoice_item as invitem
JOIN imsApp_site as site 
ON invitem.site_id = site.id 
where invitem.customer_id =  """ + str(pk) + """ ; """
    context['sites'] = columndata("", "", "", dataquery)
    # printt(pk)
    resp = {'status': 'failed', 'msg': ''}
    resp['status'] = 'success'
    return render(request, "manage_customerreport_sitewise.html", context)


def datewisecustomerinvoice(request):
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    custid = request.POST.get('custid')
    invoice = request.POST.get('invoice')
    searchresult = """ SELECT cust.name, strftime('%d/%m/%Y',DATE(recpt.date_created)) as date_created,recpt.total,recpt.deposit,recpt.balance,recpt.invoice_id
      FROM imsApp_receiptinvoice as recpt
    JOIN imsApp_customer as cust
    ON cust.id = recpt.customer_id	 
    where recpt.customer_id = """ + str(custid) + """ and recpt.date_created between '""" + str(
        fromdate) + """' and '""" + str(todate) + """' ; """
    context['invoices'] = columndata("", "", "", searchresult)
    searchtotal = """ Select
    sum(invitem.total) as total
    from imsApp_invoice_item as invitem
    where
    invitem.customer_id = """ + str(custid) + """;"""
    searchtotal = columndata("", "", "", searchtotal)

    # context['totalamounts'] = columndata("", "", "", searchtotal)

    searchdepositbalance = """SELECT sum(recpt.deposit)
		FROM imsApp_receiptinvoice as recpt
		JOIN imsApp_customer as cust
		ON cust.id = recpt.customer_id
		where recpt.customer_id = """ + str(
        custid) + """ and recpt.date_created between '""" + str(fromdate) + """' and '""" + str(todate) + """' ; """
    totaldeposit = columndata("", "", "", searchdepositbalance)
    if searchtotal[0][0]==None:
        context["totalamt"] = "0"
    else:
        context["totalamt"] = searchtotal[0][0]
    if totaldeposit[0][0]==None:
        context["totaldepositamt"] = "0"
    else:
        context["totaldepositamt"] = totaldeposit[0][0]

    # context["totalamt"] = searchtotal[0][0]
    # context["totaldepositamt"] = totaldeposit[0][0]
    context["totalbalanceamt"] = int(context["totalamt"]) - int(context["totaldepositamt"])
    resp = {'status': 'failed', 'msg': ''}
    resp['status'] = 'success'
    pdf = render_to_pdf('customerdatewiseinvoice.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
def sitewisecustomer(request):
    site = request.POST.get('site')
    custid = request.POST.get('custid')
    dataquery = """SELECT sitename from imsApp_site where id = """ + str(site) + """ ; """
    context['sitename'] = columndata("", "", "", dataquery)
    context['sitename'] = 0 if context['sitename'][0][0] == None else context['sitename'][0][0]

    dataquery = """SELECT name from imsApp_customer where id = """ + str(custid) + """ ; """
    context['customername'] = columndata("", "", "", dataquery)
    context['customername'] = 0 if context['customername'][0][0] == None else context['customername'][0][0]

    # printt(site,custid)
    searchresult = """ SELECT cust.name, strftime('%d/%m/%Y',DATE(recpt.date_created)) as date_created,recpt.total,recpt.deposit,recpt.balance,recpt.invoice_id
      FROM imsApp_receiptinvoice as recpt
    JOIN imsApp_customer as cust
    ON cust.id = recpt.customer_id
    where recpt.customer_id = """ + str(custid) + """ and recpt.site_id =""" + str(
        site) + """ ; """
    context['invoices'] = columndata("", "", "", searchresult)
    # printt(searchresult)
    searchtotal = """ Select
    sum(invitem.total) as total
    from imsApp_invoice_item as invitem
    where invitem.customer_id = """ + str(custid) + """ and invitem.site_id =""" + str(
        site) + """ ; """
    # searchtotal = columndata("", "", "", searchtotal)
    # printt(searchtotal)
    context['totalamounts'] = columndata("", "", "", searchtotal)
    # printt("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    # printt(context['totalamounts'])


    searchdepositbalance = """SELECT sum(recpt.deposit)
		FROM imsApp_receiptinvoice as recpt
		JOIN imsApp_customer as cust
		ON cust.id = recpt.customer_id
		where recpt.customer_id = """ + str(custid) + """ and recpt.site_id =""" + str(
        site) + """ ; """
    totaldeposit = columndata("", "", "", searchdepositbalance)
    if context['totalamounts']==None:
        context["totalamounts"] = "0"
        # printt("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN111")
    else:
        context["totalamounts"] =  context['totalamounts'][0][0]
        # printt("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN222")
    if totaldeposit[0][0]==None:
        context["totaldepositamt"] = "0"
    else:
        context["totaldepositamt"] = totaldeposit[0][0]

    # printt(context["totaldepositamt"])
    # context["totalamt"] = searchtotal[0][0]
    # context["totaldepositamt"] = totaldeposit[0][0]
    context["totalbalanceamt"] = int(context["totalamounts"]) - int(context["totaldepositamt"])
    resp = {'status': 'failed', 'msg': ''}
    resp['status'] = 'success'
    # printt(resp)
    pdf = render_to_pdf('customersitewiseinvoice.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def tractortotaluse(request, pk):
    # invoice = Invoice.objects.all()
    context['page_title'] = 'Invoices'
    totaluseitem = """SELECT tract.tractorno,sum(invitem.hole25),sum(invitem.hole5),sum(hole25+hole5+thussi), sum(inv.diesel),sum(invitem.thussi)
    FROM imsApp_invoice as inv
    JOIN imsApp_invoice_item as invitem
    ON inv.id = invitem.invoice_id 
	JOIN imsApp_tractor as tract
	ON inv.tractor_id = tract.id WHERE inv.tractor_id= """ + str(pk) + """;"""
    # printt(totaluseitem)
    context['totals'] = columndata("", "", "", totaluseitem)
    pdf = render_to_pdf('tractortotaluseitems.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
