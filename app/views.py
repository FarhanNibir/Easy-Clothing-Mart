from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, ChatHistory
from .forms import CustomerRegistrationForm, PasswordChangeForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.templatetags.static import static
# from static.app import product_img
import re

class Productview(View):
 def get(self, request):
  football = Product.objects.filter(category='F')
  cricket = Product.objects.filter(category='C')
  return render(request, 'app/home.html', { 'football': football,'cricket' : cricket})


class ProductDeatilView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user = user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
   return render(request, 'app/addtocart.html', {'cart': cart, 'totalamount': total_amount, 'amount': amount, 'shipingamount': shiiping_amount})
  else:
   return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))

  c.delete()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   phone_no = form.cleaned_data['phone_no']
   email = form.cleaned_data['email']
   address = form.cleaned_data['address']
   reg = Customer(user=usr, name=name, phone_no=phone_no,email=email,address=address)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Update Successfully')
  return render(request, 'app/profile.html', {'form': form})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user = request.user)
  return render(request, 'app/orders.html', {'order_placed': op})

class change_password(View):
 def get(self, request):
  form=PasswordChangeForm()
  messages.success(request, 'Congratulations!! Changed Successfully')
  return render(request, 'app/changepassword.html', {'form': form})

def football(request, data = None):
 if data == None:
  football = Product.objects.filter(category='F')
  return render(request, 'app/football.html', {'footballs': football})

def cricket(request, data = None):
  # if data == None:
  cricket = Product.objects.filter(category='C')
  return render(request, 'app/cricket.html', {'crickets': cricket})


# def buynow(request):
#  return render(request, 'app/buy-now.html')

def contactus(request):
  return render(request, 'app/contact.html')

class CustomerRegistrationView(View):
 def get (self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})

 def post(self, request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user = user)
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      total_amount = amount + shiiping_amount

  return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})

@login_required
def order_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user = user)
  for c in cart:
    OrderPlaced(user=user, customer = customer, product=c.product, quantity = c.quantity).save()
    c.delete()
  return redirect("orders")

def tryon(request):
    return render(request, 'app/try.html')


from django.http import JsonResponse

def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        try:
            # Use regular expressions to extract the product query
            search_pattern = r'(search for|find) (.+)'  # Match "search for" followed by any text
            match = re.search(search_pattern, user_message, re.IGNORECASE)
            
            if match:
                search_phrase = match.group(1)
                product_query = match.group(2).strip()

                search_results = Product.objects.filter(title__icontains=product_query)
                
                if search_results:
                    # Initialize an empty response
                    bot_response = "Here are some products I found:<br><br>"

                    # Iterate through the search results and format them
                    for product in search_results:
                        image_url = product.p_image.url
                        bot_response += f"<img src='{image_url}' alt='{product.title} Image' class='small-image'><br>"
                        bot_response += f"<strong>Name:</strong> {product.title}<br>"
                        bot_response += f"<strong>Description:</strong> {product.description}<br>"
                        bot_response += f"<strong>Price:</strong> TK.{product.selling_price}<br>"
                        bot_response += f"<strong>Discounted Price:</strong> TK.{product.discounted_price}<br><br><br>"

                else:
                    bot_response = "I couldn't find any products matching your query."

            else:
                bot_response = generate_bot_response(user_message)  # Define this function for other responses

            return JsonResponse({'bot_response': bot_response})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    return render(request, 'app/try.html')


def generate_bot_response(user_message):
    user_message = user_message.lower()
    if 'hello' in user_message:
        return 'Hello! How can I assist you today?'
    elif 'how are you' in user_message :
        return 'I am fine. How can I assist you today?'
    elif 'what is your name' in user_message or 'whats your name' in user_message or 'who are you' in user_message:
        return 'I am Alice. I am here to assist you. How can I assist you?'
    elif "bye" in user_message:
        return "Goodbye. See you."
    elif "women" in user_message or 'ladies' in user_message  or 'woman' in user_message :
       return "Here is the link of women section: <a href='http://127.0.0.1:8000/women/'>Click here</a> <br> Please checkout"
    elif "gents" in user_message or 'men' in user_message  or 'man' in user_message:
       return "Here is the link of men section: <a href='http://127.0.0.1:8000/men/'>Click here</a><br>Please checkout"
    elif "for summer" in user_message :
       return "Light and breathable fabrics like cotton and linen are perfect choices for comfortable summer wear."
    elif "my size" in user_message :
       return "Refer to our size chart for accurate measurements and fitting guidelines to determine the right size for you."
    elif "latest colours for this season" in user_message :
       return "This season's trending colours include soft pastels, earthy tones, and classic neutrals that are perfect for any wardrobe.<a href='http://127.0.0.1:8000/'>Click here</a><br>Please checkout"
    elif "change the dress" in user_message :
       return "Yes, you can. Reach our customer support team via email at support@clothingmart.com or call us."
    elif "winter clothes" in user_message :
       return "Stay warm and stylish with our cozy sweaters, comfortable jackets, and fashionable boots for a perfect winter day out.<a href='http://127.0.0.1:8000/'>Click here</a><br>Please checkout"
    elif "wash" in user_message :
       return "Follow the care instructions on the label, generally suggesting a gentle cycle with cold water and a low-heat tumble dry."
    elif "back my purchase" in user_message :
       return "Our return policy allows you to send back unworn items within 7 days of purchase for a refund or exchange."
    elif "delivery time" in user_message :
       return "Our standard delivery time is usually between 3 to 5 business days, depending on your location."
    elif "track my order" in user_message :
       return "You can track your order by using the tracking number provided in the shipping confirmation email."
    elif "customer support" in user_message or 'customer care' in user_message:
       return "You can reach our customer support team via email at support@clothingmart.com or call."
    elif "interview outfit" in user_message :
       return "For a job interview, consider wearing a well-fitted suit or a professional dress paired with subtle accessories for a polished look."
    elif "storing delicate clothes?" in user_message :
       return "Store delicate clothes in a cool, dry place, ideally in a breathable garment bag or a drawer away from direct sunlight."
    elif "sales info?" in user_message :
       return "Stay tuned for our upcoming seasonal sale event next month, where you can enjoy exciting discounts on various products."
    elif 'payment methods' in user_message :
        return 'We accept various payment methods, including credit/debit cards, PayPal, Bkash, Nagad, and other major online payment platforms for your convenience.'   
    elif 'cancel order' in user_message or 'cancel my order' in user_message:
        return 'You can cancel your order within 24 hours of placing it. After that, we recommend contacting our customer support team for further assistance.'  
    elif "hi" in user_message or 'hola' in user_message:
       return "Hello! How can I assist you today?"
    else:
        return "I'm sorry, I didn't understand that."



