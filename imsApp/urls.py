from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-password',views.update_password,name='update-password'),
    path('',views.home,name='home-page'),

    # Created by Sumit Ghumde
    path('driver',views.driver_mgt,name='driver-page'),
    path('manage_sales/<int:pk>', views.manage_sales, name='manage-sales'),
    path('manage_driver', views.manage_driver, name='manage-driver'),
    path('save_driver', views.save_driver, name='save-driver'),
    path('manage_driver/<int:pk>',views.manage_driver,name='manage-driver'),
    path('delete_driver', views.delete_driver, name='delete-driver'),
    path('show_result_driver', views.datewisedriver, name='show-result-driver'),
    path('show_result_driver/<int:pk>', views.datewisedriver, name='show-result-driver-pk'),
    path('datewisedriverreport/', views.datewisedriverreport, name='datewisedriverreport'),

    # URL For Customer Page

    path('customer', views.customer_mgt, name='customer-page'),
    path('manage_customer', views.manage_customer, name='manage-customer'),
    path('save_customer', views.save_customer, name='save-customer'),
    path('manage_customer/<int:pk>', views.manage_customer, name='manage-customer-pk'),
    path('delete_customer', views.delete_customer, name='delete-customer'),

    # URL For Helper Page

    path('helper', views.helper_mgt, name='helper-page'),
    path('manage_helper', views.manage_helper, name='manage-helper'),
    path('save_helper', views.save_helper, name='save-helper'),
    path('manage_helper/<int:pk>', views.manage_helper, name='manage-helper-pk'),
    path('delete_helper', views.delete_helper, name='delete-helper'),

    #-------------End-----------------

    path('category',views.category_mgt,name='category-page'),
    path('manage_category',views.manage_category,name='manage-category'),
    path('save_category',views.save_category,name='save-category'),
    path('manage_category/<int:pk>',views.manage_category,name='manage-category-pk'),
    path('delete_category',views.delete_category,name='delete-category'),
    path('product',views.product_mgt,name='product-page'),
    path('manage_product',views.manage_product,name='manage-product'),
    path('save_product',views.save_product,name='save-product'),
    path('manage_product/<int:pk>',views.manage_product,name='manage-product-pk'),
    path('delete_product',views.delete_product,name='delete-product'),
    path('inventory',views.inventory,name='inventory-page'),
    path('inventory/<int:pk>',views.inv_history,name='inventory-history-page'),
    path('stock/<int:pid>',views.manage_stock,name='manage-stock'),
    path('stock/<int:pid>/<int:pk>',views.manage_stock,name='manage-stock-pk'),
    path('save_stock',views.save_stock,name='save-stock'),
    path('delete_stock',views.delete_stock,name='delete-stock'),
    path('sales',views.sales_mgt,name='sales-page'),
    path('get_product',views.get_product,name='get-product'),
    path('get_product/<int:pk>/<int:sid>',views.get_product),
    path('save_sales',views.save_sales, name="save-sales"),
    path('invoices',views.invoices,name='invoice-page'),
    path('delete_invoice',views.delete_invoice,name='delete-invoice'),
    path('edit_invoice',views.edit_invoice,name='edit-invoice'),
    path('allpdf', views.allpdf, name='allpdf-page'),
    path('invoicespdf', views.invoicespdf, name='invoicespdf'),
    path('invoicescustomerpdf/<int:pk>', views.invoicescustomerpdf, name='invoicescustomerpdf'),
    path('driverspdf', views.driverpdf, name='driverspdf'),
    path('helperspdf', views.helperpdf, name='helperspdf'),
    path('tractorspdf', views.tractorpdf, name='tractorspdf'),
    path('customerspdf', views.customerpdf, name='customerspdf'),
    path('customerallbillpdf/<int:pk>', views.customerallbill, name='customerallbillpdf'),
    path('customerallbill/<int:pk>', views.customerreceiptdetails, name='customerallbill'),
    path('customerreceipt/<int:siteid>/<int:custid>/', views.customerreceipt, name='customerreceipt'),
    path('insertreceipt/', views.savenewreceipt, name='insertreceipt'),

    # URL for Tractor Page

    path('tractor', views.tractor_mgt, name='tractor-page'),
    path('manage_tractor', views.manage_tractor, name='manage-tractor'),
    path('save_tractor', views.save_tractor, name='save-tractor'),
    path('manage_tractor/<int:pk>', views.manage_tractor, name='manage-tractor-pk'),
    path('delete_tractor', views.delete_tractor, name='delete_tractor'),

    # url for items

    path('item', views.item_mgt, name='item-page'),
    path('manage_item', views.manage_item, name='manage-item'),
    path('save_item', views.save_item, name='save-item'),
    path('manage_item/<int:pk>', views.manage_item, name='manage-item-pk'),
    path('delete_item', views.delete_item, name='delete_item'),

    # url for sites

    path('site', views.site_mgt, name='site-page'),
    path('manage_site', views.manage_site, name='manage-site'),
    path('save_site', views.save_site, name='save-site'),
    path('manage_site/<int:pk>', views.manage_site, name='manage-site-pk'),
    path('delete_site', views.delete_site, name='delete_site'),


    path('totalusepdf/<int:pk>', views.totalusepdf, name='totalusepdf'),
    # path('showresult/<str:pk>', views.datewisecustomer, name='show-result'),
    path('show_result', views.datewisecustomer, name='show-result'),
    path('show_result/<int:pk>', views.datewisecustomer, name='show-result-pk'),
    path('show_result_customer', views.datewisecustomersitewise, name='show-result-customer'),
    path('show_result_customer/<int:pk>', views.datewisecustomersitewise, name='show-result-customer-pk'),

    path('datewisecustomerinvoice/', views.datewisecustomerinvoice, name='datewisecustomerinvoice'),
    path('sitewisecustomer/', views.sitewisecustomer, name='sitewisecustomer'),
    path('tractortotaluse/<int:pk>', views.tractortotaluse, name='tractortotaluse'),

]
