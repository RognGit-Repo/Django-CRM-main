class Cart():
    def __init__(self, request):
        self.session=request.session
        self.running_total=0

        cart=self.session.get('session_key')

        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        
        self.running_total=sum(float(value['price'])*int(value['p_qty']) for value in cart.values())
        
        self.cart=cart

    def add(self, product):
        product_id=str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]={'id':product.id,'name':product.name,'price': "{:.2f}".format(product.price), 'p_qty':1, 'total':"{:.2f}".format(product.price)}
        
        self.session.modified=True

    def remove(self, productId):
        del self.cart[productId]

        self.session.modified=True


    def update(self, productId, new_qty):
     
        
        if productId in self.cart:
            self.cart[productId]={'id':self.cart[productId]['id'],'name':self.cart[productId]['name'],'price': self.cart[productId]['price'], 'p_qty':int(new_qty),'total':"{:.2f}".format(float(self.cart[productId]['price'])*int(new_qty))}
        
        self.session.modified=True


    def __len__(self):
        return len(self.cart)
    

    def get_cart(self):
        return list(self.cart.values())
    

    def is_greater_1_cartItem_qty(self, key):

        return not self.cart[key]['p_qty']>1
    
    def get_running_total():
    
        pass

    





