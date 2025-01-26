from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
	
class Payment(models.Model):
	payment_method= models.CharField(max_length=15)
	amount_paid= models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )
	change= models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )

	
class Transaction(models.Model):
	# date = models.DateField()
	date=models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transactions")
	customer=models.ForeignKey(Record, on_delete=models.SET_NULL, null=True,blank=True , related_name="customer_transactions")
	payment=models.OneToOneField(Payment, on_delete=models.CASCADE)
	total_amount = models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )




class Product(models.Model):
	name=models.CharField(max_length=50)
	description=models.CharField(max_length=250)
	price=models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )
	stock_quantity=models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="categories")

    def __str__(self):
        return self.name


class Transaction_Details(models.Model):
	transaction=models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction_details")
	product=models.OneToOneField(Product,on_delete=models.SET_NULL, null=True,blank=True)
	quantity=models.IntegerField()
	unit_price=models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )
	total_price=models.DecimalField(
        max_digits=10,  # Maximum number of digits (including decimal places)
        decimal_places=2  # Number of digits after the decimal point
    )

	
