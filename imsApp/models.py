from re import I
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from more_itertools import quantify
from django.db.models import Sum


# New Edited Master models by sumit ghumde octomber 2022

class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phoneno = models.BigIntegerField()

    def __str__(self):
        return self.name


class Tractor(models.Model):
    id = models.AutoField(primary_key=True)
    tractorno = models.CharField(max_length=15)

    def __str__(self):
        return self.tractorno


class Expences(models.Model):
    id = models.AutoField(primary_key=True)
    expencesdetails = models.CharField(max_length=100)
    amount = models.IntegerField()

    def __str__(self):
        return self.Expences


class Helper(models.Model):
    id = models.AutoField(primary_key=True)
    helpername = models.CharField(max_length=50)
    phoneno = models.BigIntegerField()

    def __str__(self):
        return self.helpername


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50)
    itemdesc = models.CharField(max_length = 150)
    totalstock = models.IntegerField()

    def __str__(self):
        return self.itemname


class Customertype(models.Model):
    id = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=20)

    def __str__(self):
        return self.typename


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phoneno = models.BigIntegerField()
    def __str__(self):
        return self.name

class Site(models.Model):
    id = models.AutoField(primary_key=True)
    sitename = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.sitename

class Invoice(models.Model):
    transaction = models.CharField(max_length=250)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    helper = models.ForeignKey(Helper, on_delete=models.CASCADE)
    tractor = models.ForeignKey(Tractor,on_delete=models.CASCADE)
    diesel = models.FloatField(default=0)
    total = models.FloatField(default=0)
    ed = models.IntegerField()
    gl = models.IntegerField()
    nonel = models.IntegerField(default=0)
    df = models.IntegerField(default=0)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.transaction

    def item_count(self):
        return Invoice_Item.objects.filter(invoice=self).aggregate(Sum('quantity'))['quantity__sum']


class Invoice_Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hole25 = models.FloatField(default=0, blank=True)
    hole5 = models.FloatField(default=0, blank=True)
    thussi = models.FloatField(default=0, blank=True)
    price = models.FloatField(default=0, blank=True)
    deposit = models.FloatField(default=0, blank=True)
    balance = models.FloatField(default=0, blank=True)
    quantity = models.FloatField(default=0, blank=True)
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    total = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.invoice.transaction

class Receiptinvoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,default=1)
    total = models.FloatField(default=0)
    deposit = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    # stockistname = models.CharField(max_length=2, blank=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
# For Item Stock Baalance models

class ItemStockBalance(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stockqty = models.FloatField(default=0)
    stockistname = models.CharField(max_length=2, blank=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    # def __str__(self):
    #     return self.itemname


# End Item Stock Balance Models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.code + ' - ' + self.name

    def count_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == '1':
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available = stockIn - stockOut
        return available


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    type = models.CharField(max_length=2, choices=(('1', 'Stock-in'), ('2', 'Stock-Out')), default=1)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.code + ' - ' + self.product.name

# class Invoice(models.Model):
#     transaction = models.CharField(max_length = 250)
#     customer = models.CharField(max_length = 250)
#     total = models.FloatField(default= 0)
#     date_created = models.DateField(default=timezone.now)
#     date_updated = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.transaction
#
#     def item_count(self):
#         return Invoice_Item.objects.filter(invoice = self).aggregate(Sum('quantity'))['quantity__sum']
#
# class Invoice_Item(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank= True, null= True)
#     price = models.FloatField(default=0)
#     quantity = models.FloatField(default=0)
#
#     def __str__(self):
#         return self.invoice.transaction


# @receiver(models.signals.post_save, sender=Invoice_Item)
# def stock_update(sender, instance, **kwargs):
#     stock = Stock(product=instance.product, quantity=instance.quantity, type=2)
#     stock.save()
#     # stockID = Stock.objects.last().id
#     Invoice_Item.objects.filter(id=instance.id).update(stock=stock)
#
#
# @receiver(models.signals.post_delete, sender=Invoice_Item)
# def delete_stock(sender, instance, **kwargs):
#     try:
#         stock = Stock.objects.get(id=instance.stock.id).delete()
#     except:
#         return instance.stock.id


# @receiver(models.signals.post_save, sender=Invoice)
# def item_stock_update(sender, instance, **kwargs):
#
#     stock = Item(itemname=instance.itemname, totalstock=instance.quantity)
#     stock.save()
#     # stockID = Stock.objects.last().id
#     Invoice_Item.objects.filter(id=instance.id).update(stock=stock)
