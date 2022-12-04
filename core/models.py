from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField


CATEGORY = (
    ('K', 'Kits'),
    ('BA', 'Balls'),
    ('A', 'Accessories'),
    ('F','Footwear'),
    ('BG','Bags'),
)

LABEL = (
    ('S','Standard'),
    ('NA', 'New Arrival'),
    ('BS', 'Best Seller'),
    ('U','Used')
)


class Item(models.Model) :
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=2)
    image_link = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"pk" : self.pk}
        )

    def get_add_to_cart_url(self) :
        return reverse("core:add-to-cart", kwargs={"pk" : self.pk}
        )

    def get_remove_from_cart_url(self) :
        return reverse("core:remove-from-cart", kwargs={"pk" : self.pk}
        )


#Add OrderItem model to store data of the product(s) you want to order.
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


#Add Order model to store data of the product(s) ordered.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        shipping = 9.99
        for order_item in self.items.all():
            total += order_item.get_final_price()
        tax = 0.04*total
        return round(total+shipping+tax,2)
    
    def get_tax(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        tax = 0.04*total
        return round(tax,2)

    def get_items(self):
        return self.items.all()

    def get_price(self):
        final_price_list = []
        for order_item in self.items.all():
            final_price_list.append(order_item.get_final_price())
        return final_price_list

#Add CheckoutAddress model to store the shipping address of the order from the form we made before.
class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

#Make Payment class to save pasyment information using stripe.
class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username