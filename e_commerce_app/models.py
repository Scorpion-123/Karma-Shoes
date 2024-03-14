from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class brand(models.Model):
    brand_name = models.CharField(max_length = 30)

    def __str__(self):
        return self.brand_name


class Shoe(models.Model):
    name = models.CharField(max_length = 50)
    desc = models.TextField()
    price = models.IntegerField()
    is_exclusive = models.BooleanField(default = False)
    image = models.ImageField(upload_to='shoe_images/')

    brand = models.ForeignKey(brand, on_delete = models.CASCADE) 

    def __str__(self):
        return self.name
        


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.shoe.name} | {self.user.username}"
    

class ShoeComments(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete = models.CASCADE)

    author_name = models.CharField(max_length = 100)
    author_email = models.EmailField()

    review = models.TextField()
    review_star = models.IntegerField()

    def __str__(self):
        return f"{self.author_name} | {self.shoe.name}"
    



class Order(models.Model):
    order_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    all_shoes = models.BinaryField()                  # This field is storing the whole cart object of a user in the form of a list.
    
    name = models.CharField(max_length = 100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length = 500)
    pin_code = models.IntegerField()
    order_notes = models.TextField()

    order_value = models.DecimalField(decimal_places = 2, max_digits = 10)
    is_paid = models.BooleanField(default = False)
    order_date = models.DateTimeField(null=True)


    def __str__(self):
        return f"{self.order_id} | {self.user}"