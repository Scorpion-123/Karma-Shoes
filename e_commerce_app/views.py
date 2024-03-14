from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import random
import pickle
from datetime import datetime


# Helper functions that are required for calculating the discounted price of the shoes.
def get_discount(price, discount_percentage):
        discount = discount_percentage/100 * price
        return price - discount


def get_price_list(shoe_list):
    prices = []
    for shoe in shoe_list:
        prices.append(shoe.price)

    return prices


def get_discount_list(shoes_list):
    discount_list = []

    for shoe in shoes_list:
        if (shoe.price >= 6000 and shoe.price <= 8999):
            discount_list.append(10)
        
        elif (shoe.price >= 9000):
             discount_list.append(12)
        
        else:
             discount_list.append(5)

    return discount_list


# Create your views here.
def index_page(request):
    
    all_shoes = Shoe.objects.filter(is_exclusive = False)
    
    shoes1 = all_shoes[0:8]
    shoe_price_list1 = get_price_list(shoes1)     # This returns the price list of all the shoes.
    discount_list1 = get_discount_list(shoes1)    # This returns the list of calculated discount's as per the shoe price.
    discounted_shoe_price1 = list(map(get_discount, shoe_price_list1, discount_list1))      # This performs the discount calculation on the shoe, and returns the disocunted_shoe_prices.

    
    shoes2 = all_shoes[8:16]
    shoe_price_list2 = get_price_list(shoes2)     # This returns the price list of all the shoes.
    discount_list2 = get_discount_list(shoes2)    # This returns the list of calculated discount's as per the shoe price.
    discounted_shoe_price2 = list(map(get_discount, shoe_price_list2, discount_list2))      # This performs the discount calculation on the shoe, and returns the disocunted_shoe_prices.


    exclusive_shoes = Shoe.objects.filter(is_exclusive = True)    # This are for the exclusive shoes that are displayed in the exclusive section.
    shoe_price_list_ex = get_price_list(exclusive_shoes)
    discount_list_ex = get_discount_list(exclusive_shoes)
    discounted_price_ex = list(map(get_discount, shoe_price_list_ex, discount_list_ex))

    return render(request, 'index.html', context= {'shoes_discount': zip(shoes1, discounted_shoe_price1), 
                                                   'shoes_discount2': zip(shoes2, discounted_shoe_price2),
                                                   'shoes_discount_ex': zip(exclusive_shoes, discounted_price_ex)})




def logout_user(request):
    logout(request)
    return redirect('home')


def is_unique_username(users_list, current_username):
    for user in users_list:
        if (user.username == current_username):
            return False

    return True

def is_unique_email(users_list, current_email):
    for user in users_list:
        if (user.email == current_email):
            return False

    return True


def login_user(request):
    if (request.method == 'POST'):
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Please Enter You're Credentials Correctly.")
        

    return render(request, 'login.html')


def add_to_cart(request, pk):
    
    if (request.user.is_anonymous):
        messages.warning(request, "The User Must Be LoggedIn, in order to add a product to the Cart.")
        return redirect('login')

    user = request.user
    shoe = Shoe.objects.get(pk=pk)
    new_cart = Cart(user=user, shoe=shoe)
    new_cart.save()
    
    messages.info(request, f"The Shoe : {shoe.name} has been successfully added to cart.")
    return redirect('home')



# Very Important Function that handels all the cart functionalities.
coupon_already_applied = False
current_coupon = ""
shipping_charge = 0
total_cost = 0

def view_cart(request):
    global coupon_already_applied
    global current_coupon
    global shipping_charge
    global total_cost

    free_shipping = True
    is_cart_empty = False

    user = request.user
    cart_items = Cart.objects.filter(user=user)  # This will return all the cart items, but we need to have the shoe items.
    shoe_items = []
    for i in cart_items:
        shoe_items.append(i.shoe)

    shoe_price = get_price_list(shoe_items)
    discount_list = get_discount_list(shoe_items)
    discounted_price = list(map(get_discount, shoe_price, discount_list))
    total = sum(discounted_price)

    
    # Check whether the cart is empty or not.
    if (len(cart_items) == 0):
        is_cart_empty = True 


    # Calculate Shipping Charge. (END STEP)
    if (total < 50000):
        free_shipping = False
        shipping_charge = (0.85/100) * total
    else:
        shipping_charge = 0


    if (request.method == 'POST'):

        # This will signify that if the cart is empty then nobody should be eligible to apply any kind of coupon code.
        if (is_cart_empty):
            messages.info(request, "No Coupon Can Be Applied to An Empty Cart.So Go Shop Now...")
            return redirect('view_cart')
        

        coupon_code = request.POST.get('coupon').upper()
        if (ascii(coupon_code) == ascii('HELLO123')):                 # This is the case when the user enters the correct coupon code.
            total = total - ((20/100) * total)
            current_coupon = coupon_code
            coupon_already_applied = True
            messages.info(request, f"Coupon '{coupon_code}' added Successfully.")


        elif (ascii(coupon_code) == ascii('FREE SHIPPING')):
            free_shipping = True
            current_coupon = coupon_code
            shipping_charge = 0
            coupon_already_applied = True
            messages.info(request, f"Coupon '{coupon_code}' added Successfully.")


        elif (ascii(coupon_code) == ascii(f'COUPON : {current_coupon}')):      # When the user wants to remove the already entered coupon code.
            coupon_already_applied = False
            messages.info(request, "Coupon Removed Successfully.")


        else:                                                         # Wrong Coupon Code.
            messages.warning(request, "Invalid Coupon Code.")

    # This is globally available and is majorly used by the checkout funtion in order to fetch all the price details about the shoe's that are present in the cart.
    
    total = round(total, 2)
    total_cost = total
    return render(request, 'cart.html', context={'cart_items': zip(cart_items, discounted_price, discount_list), 
                                                 'total': total,
                                                 'current_coupon': current_coupon,
                                                 'coupon_applied': coupon_already_applied,
                                                 'free_shipping': free_shipping,
                                                 'shipping_charge': round(shipping_charge, 2),
                                                 'is_cart_empty': is_cart_empty})



def remove_item_from_cart(request, pk):
    cart = Cart.objects.get(pk = pk)
    cart.delete()
    messages.info(request, f"'{cart.shoe.name}' has been successfully removed from cart.")

    return redirect('view_cart')



def rating_calculation(review_list):
    result = 0
    
    if (len(review_list) == 0):
        return result

    for review in review_list:
        result += review.review_star

    return (result / len(review_list))


# This funtion handels the url to display each shoe. (Elaborated Design)
def display_each_shoe(request, pk):

    shoe = Shoe.objects.get(pk = pk)
    discount_percentage = get_discount_list([shoe])[0]
    discounted_price = get_discount(shoe.price, discount_percentage)

    if (request.method == "POST"):

        if (request.user.is_anonymous):
            messages.info(request, "The User Must Be LoggedIn, in order to give a review.")
            return redirect('login')

        author_name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        new_comment = ShoeComments(shoe = shoe, author_name = author_name, author_email = email, review = review, review_star = rating)
        new_comment.save()
        messages.info(request, "New Review Has Been Posted Successfully.")
        
    
    # The comments should be fetched after the comments are being posted so that the recent comments also show up on the console.
    # This will bring us if there are any comments about the shoe with the desired primary key as supplied by the user.
    comments = ShoeComments.objects.filter(shoe__id = pk)
    are_comments_present = True

    if (len(comments) == 0):
        are_comments_present = False
    
    product_rating = round(rating_calculation(comments), 1)

    return render(request, 'each_shoe.html', context = {'shoe': shoe,
                                                        'discount_price' : discounted_price,
                                                        'discount_percentage': discount_percentage,
                                                        'comments': comments,
                                                        'comments_present': are_comments_present,
                                                        'product_rating': product_rating})




# This is a helper function for the checkout, this will generate a unique order id for the order.
def generate_unique_order_id(OrderList):
    order_id = 0
    if (len(OrderList) == 0):
        order_id = random.randint(1000000, 9999999) 
    
    else:

        while (True):
            temp_id = random.randint(1000000, 9999999) 
            item = OrderList.filter(order_id = temp_id)

            if (len(item) == 0):
                order_id = temp_id
                break;

    return order_id


order_confirmed_context = {}
def checkout(request):

    global order_confirmed_context
        
    if (request.user.is_anonymous):
        messages.warning(request, "You Must Be Logged In.")
        return redirect('login')
    
    first_name, last_name = request.user.get_full_name().split()
    email = request.user.email

    ship_charge = shipping_charge

    user = request.user
    cart_items = Cart.objects.filter(user=user)  # This will return all the cart items, but we need to have the shoe items.
    shoe_items = []
    for i in cart_items:
        shoe_items.append(i.shoe)

    shoe_price = get_price_list(shoe_items)
    discount_list = get_discount_list(shoe_items)
    discounted_price = list(map(get_discount, shoe_price, discount_list))
    # total_cost = round(sum(discounted_price), 2)


    if (request.method == 'POST'):
        first_name_post = request.POST.get('first_name')
        last_name_post = request.POST.get('last_name')
        email_post = request.POST.get('email')
        number = request.POST.get('number')
        country = request.POST.get('country')
        address_post = request.POST.get('add1')
        city = request.POST.get('city')
        pincode = request.POST.get('zip')
        instruction = request.POST.get('message')

        # If any of the field is missing then we cannot proceed with the shipping. Hence we will return to the same page with a warning message.
        if ((ascii(number) == ascii('')) or (ascii(country) == ascii('')) or (ascii(address_post) == ascii('')) or (ascii(city) == ascii('')) or (ascii(pincode) == ascii(''))):
            messages.warning(request, "All The Details are important for shipping, Please Fill Then Carefully and try again.")
            return redirect('checkout')
        

        # Select Country, because the values of the country's come as integer.
        if (country == '1'):
            country = "India"
        elif (country == '2'):
            country = "Dubai"
        else:
            country = "USA"
        
        order_id = generate_unique_order_id(Order.objects.all())
        # If all the fields are present then we can successfully place an order.
        new_order = Order(order_id = order_id,
                          user = request.user,

                          all_shoes = pickle.dumps(cart_items),              # Here we're dumping the current cart of the user when we're placing an order.
                          
                          name = f"{first_name_post} {last_name_post}",
                          phone_number = number,
                          email = email_post,
                          address = f"{address_post}, {city}, {country}",
                          pin_code = pincode,
                          order_notes = instruction,
                          order_value = total_cost + round(shipping_charge, 2),
                          is_paid = True,
                          order_date = datetime.now())
        
        new_order.save()
        messages.info(request, "Your Order Has Been Placed Successfully.")
        
        order_confirmed_context = {'first_name':first_name,
                                   'order_id' : order_id, 
                                   'last_name': last_name,
                                   'email': email,
                                   'address': address_post,
                                   'city': city,
                                   'country': country,
                                   'pin_code': pincode,
                                   'all_shoes_price': zip(shoe_items, discounted_price),
                                   'subtotal': total_cost,
                                   'shipping': round(shipping_charge, 2),
                                   'total': round(total_cost + shipping_charge, 2),
                                   'coupon_status': coupon_already_applied,
                                   'coupon_code': current_coupon}
        

        # After the order has been placed successfully, the cart should be empty and should not contain any product.
        current_cart = Cart.objects.filter(user = request.user)
        for element in current_cart:
            element.delete()


        return redirect('order_confirmed')


    
    return render(request, 'checkout.html', context={'first_name':first_name,
                                                     'last_name': last_name,
                                                     'email': email,
                                                     'all_shoes_price': zip(shoe_items, discounted_price),
                                                     'subtotal': total_cost,
                                                     'shipping': round(shipping_charge, 2),
                                                     'total': round(total_cost + shipping_charge, 2),
                                                     'coupon_status': coupon_already_applied,
                                                     'coupon_code': current_coupon})


# This is to display the order confirmation page.(Our Order has been confirmed)
def order_confirmed(request):
    
    return render(request, "order_confirmation.html", context=order_confirmed_context)



# This is to view the Total Order's given and the page for specific order.
def view_order(request):
    
    if (request.user.is_anonymous):
        messages.info(request, "User Must Be Logged IN to View there Order.")
        return redirect('login')
    

    is_order_list_empty = False
    order_list = Order.objects.filter(user = request.user)
    
    if (order_list.count() == 0):
        is_order_list_empty = True

    return render(request, "view_orders.html", context={
                                                            'orders': order_list,
                                                            'is_order_list_empty': is_order_list_empty,
    })



def view_single_order(request, order_id):
    
    order = Order.objects.get(order_id = order_id)
    return render(request, "view_single_order.html", context = {
                                                                    'order': order,
    })


def view_all_shoes_by_category(request):

    shoes = Shoe.objects.all()
    brands = brand.objects.all()

    # If a person is clicking a particular brand on the brand column then the brand name will be fetched and the shoes of that particular brand will be displayed.
    if (request.method == 'GET'):
        brand_name = request.GET.get('brand')
        if (brand_name is not None):
            shoes = Shoe.objects.filter(brand__brand_name = brand_name)

    # This is to sort the shoes by specific price tags.(either from High To Low or Low To High)
    if (request.method == 'GET'):
        category = request.GET.get('price')
        if (category == 'htl'):
            shoes = shoes.order_by('-price')
        elif (category == 'lth'):
            shoes = shoes.order_by('price')


    shoe_prices = get_price_list(shoes)
    discount_list = get_discount_list(shoes)
    discount_prices = list(map(get_discount, shoe_prices, discount_list))

    return render(request, "all_shoes.html", context = {
                                                            'shoes': zip(shoes, discount_prices),
                                                            'brands': brands,
                                                            'count': shoes.count(),
    })


