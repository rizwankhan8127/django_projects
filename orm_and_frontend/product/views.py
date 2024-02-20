from django.shortcuts import render,redirect
from django.http import HttpResponse
from product.models import ProductTable,CartTable,OrderTable,CustomerDetails
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import calendar
from django.shortcuts import get_object_or_404



# Create your views here.
def index(request):
   data={}
   #ProductTable.objects.all() this will fetch non active product also. so it is better to use filter
   user_id=request.user.id
   id_specific_cartitems=CartTable.objects.filter(uid=user_id)
   #couting total items in cart
   count=id_specific_cartitems.count()
   data['cart_count']=count
   fetched_products=ProductTable.objects.filter(is_active=True)
   data['products']=fetched_products
   return render(request,'product/index.html',context=data)

def filter_by_category(request,category_value):
   #select * from product where is_active=True and category=category_value;
   #ProductTable.objects.filter(is_active=True , category=category_value)
   #from django.db.models import Q
   data={}
   q1 = Q(is_active=True)
   q2 = Q(category=category_value)
   filterd_products=ProductTable.objects.filter(q1 & q2)
   data['products']=filterd_products
   return render(request,'product/index.html',context=data)

def sort_by_price(request,sort_value):
   #select * from product order by salary desc;
   data={}
   if sort_value=='asc':
      price = 'price'
   else:
      price = '-price'
   sorted_products=ProductTable.objects.filter(is_active=True).order_by(price)
   data['products']=sorted_products
   return render(request,'product/index.html',context=data)

def filter_by_rating(request,rating_value):
   #select * from product where is_active=True and category=category_value;
   #ProductTable.objects.filter(is_active=True , category=category_value)
   #from django.db.models import Q
   data={}
   q1 = Q(is_active=True)
   q2 = Q(rating__gt=rating_value)
   filterd_products=ProductTable.objects.filter(q1 & q2)
   data['products']=filterd_products
   return render(request,'product/index.html',context=data)


def filter_by_price_range(request):
   data={}
   min = request.GET['min']
   max = request.GET['max']
   q1 = Q(price__gte=min)
   q2 = Q(price__lte=max)
   q3 = Q(is_active=True)
   filterd_products=ProductTable.objects.filter(q1 & q2 & q3)
   data['products']=filterd_products
   return render(request,'product/index.html',context=data)

def product_details(request,pid):
   product=ProductTable.objects.get(id=pid)
   return render(request,'product/product_details.html',{'product':product})

def register_user(request):
   data = {}
   if request.method=="POST":
      uname=request.POST['username']
      upass=request.POST['password']
      uconf_pass=request.POST['password2']
      if(uname=='' or upass=='' or uconf_pass==''):
         data['error_msg']='Fields cannot be empty'
         return render(request,'user/register.html',context=data)
      elif(upass!=uconf_pass):
         data['error_msg']='Password and Confirm password does not matched'
         return render(request,'user/register.html',context=data)
      else:
         user=User.objects.create(username=uname)
         user.set_password(upass)
         user.save()
         customer=CustomerDetails.objects.create(uid=user)
         customer.save()
         return redirect('/user/login')
   return render(request,'user/register.html')   

def login_user(request):
   data={}
   if request.method=="POST":
      uname=request.POST['username']
      upass=request.POST['password']
      if (uname=='' or upass==''):
         data['error_msg']='Fields can not be empty '
         return render(request,'/user/login.html',context=data)
      elif(not User.objects.filter(username=uname).exists()):
         data['error_msg']= uname + 'user is not registered'
         return render (request,'/user/login.html' ,context=data)
      else:
         user=authenticate(username=uname,password=upass)
         print(user)
         if user is not None:
            login(request,user)
            return redirect('/product/index')
         else:
            data['error_msg']='Wrong Password'
            return render(request,'user/login.html',context=data)
   return render(request,'user/login.html')

def user_logout(request):
   logout(request)
   return redirect('/product/index')

def add_to_cart(request,pid):
   if request.user.is_authenticated:
      uid = request.user.id
      print("user id = " ,uid)
      print("product id = ", pid)
      #we cant pass only id in cart table, it is expecting object of User and Product
      #therefore below line will gives error
      #cart=CartTable.objects.create(pid=pid,uid=uid)
      user=User.objects.get(id=uid)
      product=ProductTable.objects.get(id=pid)
      
      q1 = Q(uid=uid)
      q2 = Q(pid=pid)
      available_products=CartTable.objects.filter(q1 & q2)
      print()
      if(available_products.count()>0):
         messages.error(request, 'Product is alredy in the cart.')
         return redirect('/product/index') 
      else:
         cart=CartTable.objects.create(pid=product,uid=user)
         cart.save()
         messages.success(request,"Product is added to the cart.")
         return redirect('/product/index')  
   else:
      return redirect("/user/login")      
      
def view_cart(request):
   data ={}
   user_id=request.user.id
   user=User.objects.get(id = user_id)
   id_specific_cartitems=CartTable.objects.filter(uid=user_id)
   data['products']=id_specific_cartitems
   data['user']=user
   #couting total items in cart
   count=id_specific_cartitems.count()
   # data['cart_count']=count
   #couting total price of cart
   total_price = 0
   total_quantity=0
   for item in id_specific_cartitems:
      #print(item.pid.price)
      # total_price+=item.pid.price
      total_price=(total_price+item.pid.price)*(item.quantity)
      total_quantity+=item.quantity
   data['total_price']=total_price
   data['cart_count']=total_quantity
   # print(data['cart_count'])
   return render(request,'product/cart.html',context=data)

def remove_item(request,cartid):
   cart=CartTable.objects.get(id=cartid)
   cart.delete()
   return  redirect('/product/view_cart')

def update_quantity(reqest,flag,cartid):
   cart=CartTable.objects.filter(id=cartid)
   actual_quantity = cart[0].quantity
   if(flag=="1"):
      cart.update(quantity=actual_quantity + 1)
      pass
   else:
      if(actual_quantity>1):
         cart.update(quantity=actual_quantity-1)
      pass
   return redirect('/product/view_cart')
# def place_order(request):
#    current_GMT=time.gmtime()
#    time_stamp=calendar.timegm(current_GMT)
#    user_id=request.user.id
#    oid=str(user_id)+"-"+str(time_stamp)
#    cart=CartTable.objects.filter(uid=user_id)
#    for data in cart:
#       order=OrderTable.objects.create(order_id=oid,quantity=data.quantity,pid=data.pid,uid=data.uid)
#       order.save()
#    return HttpResponse("Order Placed")
def place_order(request):
   data={}
   user_id=request.user.id
   user=User.objects.get(id=user_id)
   id_specific_cartitems=CartTable.objects.filter(uid=user_id)
   # customer=CustomerDetails.objects.get(uid=user_id)
   # data['customer']=customer
   data['products']=id_specific_cartitems
   data['user']=user
   total_price=0
   total_quantity=0
   for item in id_specific_cartitems:
      total_price=(total_price+item.pid.price)*(item.quantity)
      total_quantity+=item.quantity
   data['total_price']=total_price
   data['cart_count']=total_quantity
   return render(request,'product/order.html',context=data)   

def edit_profile(request):
    data = {}
    user_id = request.user.id
    customer = get_object_or_404(CustomerDetails, uid=user_id)  # Using get_object_or_404 to handle the case where no objects are found
    data['customer'] = customer
    
    if request.method == 'POST':
        # Retrieve POST data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_type = request.POST.get('address_type')
        full_address = request.POST.get('full_address')
        pincode = request.POST.get('pincode')
        
        # Update customer details
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.address_type = address_type
        customer.full_address = full_address
        customer.pincode = pincode
        customer.save()  # Save the changes
        
        return redirect('/product/index')
    
    return render(request,"user/edit_profile.html",context=data)


