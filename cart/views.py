from django.shortcuts import render, redirect,get_object_or_404
from .cart import Cart
from website.models import Product
from django.http import JsonResponse
import json
from django.db import transaction, connection

# Create your views here.
def cart_add(request):
    cart=Cart(request)

    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))

        product=get_object_or_404(Product, id=product_id)

        cart.add(product=product)

        cart_qty=cart.__len__()
        cart.running_total=sum(float(value['price'])*int(value['p_qty']) for value in cart.cart.values())
        response=JsonResponse({'qty': cart_qty, 'cart':json.dumps(cart.get_cart()), 'running_total':cart.running_total})
        print(cart.running_total, cart.cart)
        return response

def cart_delete(request):
    cart=Cart(request)

    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))
        cart.remove(productId=str(product_id))
        cart_qty=cart.__len__()
        cart.running_total=sum(float(value['price'])*int(value['p_qty']) for value in cart.cart.values())
        response=JsonResponse({'qty': cart_qty, 'cart':json.dumps(cart.get_cart()), 'running_total':cart.running_total})
        print(cart.running_total, cart.cart)
        return response

def cart_update(request):
    cart=Cart(request)

    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))
        new_qty=request.POST.get('new_qty')
        cart.update(productId=str(product_id), new_qty=new_qty)
        cart_qty=cart.__len__()
        cart.running_total=sum(float(value['price'])*int(value['p_qty']) for value in cart.cart.values())
        response=JsonResponse({'qty': cart_qty, 'cart':json.dumps(cart.get_cart()), 'running_total':cart.running_total})
        print(cart.running_total, cart.cart)
        return response



#Transactional query to handle concurrent transactions/race conditions
def process_sale(request):
    cart=Cart(request)
    # Start a transaction block with isolation level set to SERIALIZABLE
    with transaction.atomic():
        # Optionally, set the isolation level to SERIALIZABLE for this specific transaction
        with connection.cursor() as cursor:
            cursor.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')
        
        for itemkey, itemValue in cart.cart.items:

            # Lock the product row using pessimistic locking (select_for_update)
            product = Product.objects.select_for_update().get(id=itemValue['id'])
            
            # Check if inventory is sufficient for the sale
            if product.stock_quantity >= itemValue['p_qty']:
                # **Locally Update** the product's fields before saving
                product.stock_quantity -= itemValue['p_qty']  # Deduct the sale quantity from stock
                
                # Optionally, update other fields or properties if needed
                # For example, apply a discount, or calculate the sale price
                # product.total_value = product.price * product.quantity_in_stock  # This is just an example

                # Create a sale record to reflect the transaction
                Sale.objects.create(product=product, quantity=sale_qty, price=product.price)

                # Save the updated product back to the database (commit the changes)
                product.save()

                # Return a success response (e.g., render a template showing the updated product)
                return render(request, 'sale_success.html', {'product': product})
            else:
                # If not enough inventory, return a failure response
                return render(request, 'sale_failed.html', {'product': product})



#         Breakdown:
# Transaction Block (transaction.atomic()):

# We start by using transaction.atomic(), which creates a database transaction. All database operations inside this block will be treated as a single unit, and if an exception occurs, all changes will be rolled back to ensure consistency.
# Inside this block, we execute raw SQL with SET TRANSACTION ISOLATION LEVEL SERIALIZABLE to set the isolation level to SERIALIZABLE for this specific transaction, ensuring the strictest data consistency rules are applied.
# Pessimistic Locking (select_for_update()):

# We use select_for_update() to lock the product row for the product being sold. This ensures that no other transaction can modify this product's data (including quantity) until the current transaction completes.
# select_for_update() will lock the row at the database level, preventing other transactions from changing the product while we're processing the sale.
# Locally Update Fields:

# After locking the product, we check if the quantity_in_stock is sufficient to process the sale.
# We update the quantity_in_stock field locally by subtracting the sale_qty from it. This change does not yet affect the database until we call save().
# You can also perform additional logic locally, such as updating other fields (like total_value or applying discounts) or calculating new values before saving the model instance.
# Saving the Changes (product.save()):

# Once the transaction block is executed, and we have made our updates locally, we call product.save() to persist the updated quantity_in_stock back to the database.
# Since we are inside a transaction, the change will only be committed when the transaction.atomic() block successfully completes. If something goes wrong (e.g., insufficient stock, database error), the changes will be rolled back automatically.
# Creating a Sale Record:

# We also create a Sale object to record the sale. This sale references the Product and includes the quantity sold, which allows you to keep track of the transaction.
# Handling Response:

# After the transaction is successful, we render a success template (sale_success.html) showing the updated product.
# If there is not enough inventory, we render a failure template (sale_failed.html).
# Why This Approach Works:
# Pessimistic Locking (select_for_update()) ensures that if two users try to sell the same product at the same time, the database will prevent both from modifying the same row concurrently.
# Transaction Isolation Level (SERIALIZABLE) ensures that no other transactions can read or write to the product's inventory during the current transaction, avoiding conflicts with phantom reads or dirty data.
# Locally Updating Fields allows you to modify the quantity_in_stock (or any other fields) in memory, and once you're ready, you can save these changes back to the database when the transaction is complete.
# Atomic Transactions ensure that the entire operation (locking, checking stock, updating fields, saving the product, and creating the sale) is treated as a single unit — if anything fails, all changes are rolled back.
# Final Thoughts:
# This approach provides a robust and reliable mechanism for managing concurrent transactions involving inventory updates, especially when stock levels need to be handled safely in a multi-user environment. The use of pessimistic locking prevents race conditions, and the transaction isolation level ensures that the database behaves predictably under concurrent access.

# Would you like further clarification on any specific part of the code or concepts?