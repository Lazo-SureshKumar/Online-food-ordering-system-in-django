from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import models
from . import forms
from django.contrib.auth.models import Group
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Customer,Items,Order,OrderedItem,Feedback
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from .forms import  CustomerUserForm,CustomerForm


# user after login
def index(request):
    Item = Items.objects.all()
    context={
        'menuitem':Item
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context,request))

# user before login 
def home(request):
    Item = Items.objects.all()
    context={
        'menuitem':Item
    }
    template = loader.get_template('index.html')
    if request.user.is_authenticated:
        return HttpResponseRedirect('index')
    return HttpResponse(template.render(context,request))


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('home')
    else:
        return redirect('admin-dashboard')

# admin dashboard
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=Customer.objects.all().count()
    itemcount=Items.objects.all().count()
    ordercount=Order.objects.all().count()
    # for recent order tables
    orders=Order.objects.all()
    ordered_items=[]
    ordered_bys=[]
    for order in orders:
        ordered_item=Items.objects.all().filter(id=order.item.id)
        ordered_by=Customer.objects.all().filter(id = order.customer.id)
        ordered_items.append(ordered_item)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'itemcount':itemcount,
    'ordercount':ordercount,
    'data':zip(ordered_items,ordered_bys,orders),
    }
    return render(request,'admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=Customer.objects.all()
    return render(request,'admin_view_customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    userForm = CustomerUserForm(instance=user)
    customerForm = CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm = CustomerUserForm(request.POST,instance=user)
        customerForm = CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save(commit=False)
            raw_password = userForm.cleaned_data['password']
            user.set_password(raw_password)
            user.save()
            login(request,user)
            customerForm.save()
            return redirect('view-customer')
    return render(request,'admin_update_customer.html',context=mydict)

# admin view the item
@login_required(login_url='adminlogin')
def admin_items_view(request):
    items=Items.objects.all()
    return render(request,'admin_item.html',{'items':items})


# admin add item by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_item_view(request):
    itemForm=forms.ItemForm()
    if request.method=='POST':
        itemForm=forms.ItemForm(request.POST, request.FILES)
        if itemForm.is_valid():
            itemForm.save()
        return HttpResponseRedirect('admin-items')
    return render(request,'admin_add_item.html',{'itemForm':itemForm})


@login_required(login_url='adminlogin')
def delete_item_view(request,pk):
    Item=Items.objects.get(id=pk)
    Item.delete()
    return redirect('admin-items')


@login_required(login_url='adminlogin')
def update_item_view(request,pk):
    item=Items.objects.get(id=pk)
    itemForm=forms.ItemForm(instance=item)
    if request.method=='POST':
        itemForm=forms.ItemForm(request.POST,request.FILES,instance=item)
        if itemForm.is_valid():
            itemForm.save()
            return redirect('admin-items')
    return render(request,'admin_update_item.html',{'itemForm':itemForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=Order.objects.all()
    ordered_items=[]
    ordered_bys=[]
    for order in orders:
        ordered_item=Items.objects.all().filter(id=order.item.id)
        ordered_by=Customer.objects.all().filter(id = order.customer.id)
        ordered_items.append(ordered_item)
        ordered_bys.append(ordered_by)
    return render(request,'admin_view_booking.html',{'data':zip(ordered_items,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=Order.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=Order.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    query = request.GET['query']
    items=Items.objects.all().filter(name__icontains=query)
    word = ''
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter=item_ids.split('|')
        item_count_in_cart=len(set(counter))
    else:
        item_count_in_cart=0
        for item in items:
            word="Searched Result :"+item.name

    if request.user.is_authenticated:
        return render(request,'home.html',{'menuitem':items,'word':word,'item_count_in_cart':item_count_in_cart})
    return render(request,'index.html',{'menuitem':items,'word':word,'item_count_in_cart':item_count_in_cart})



def signup(request):
    userForm= CustomerUserForm()
    customerForm= CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm= CustomerUserForm(request.POST)
        customerForm= CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'signup.html',context=mydict)

def login_view(request):
    data = {'title':'Login to your account'}
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        if not (username and password):
            messages.error(request,'All fields are mandatory')
            return redirect('login')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('user logged in') 
                nextUrl = request.POST.get('next')
                print(nextUrl)
                if not nextUrl:
                    nextUrl = 'index'
                return redirect(nextUrl)
        messages.error(request,'Invalid credentials')
        return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def add_view(request,pk):
    if request.user.is_authenticated:
        Item=Items.objects.all()
        #for cart counter, fetching Item ids added by customer from cookies
        if 'Item_ids' in request.COOKIES:
            print(request.COOKIES)
            Item_ids = request.COOKIES['Item_ids']
            print(request.COOKIES['Item_ids'])
            counter=Item_ids.split('|')
            Items_count_in_cart=len(set(counter))
        else:
            Items_count_in_cart=1
        response = HttpResponseRedirect('home')
        #adding item id to cookies
        if 'Item_ids' in request.COOKIES:
            Item_ids = request.COOKIES['Item_ids']
            if Item_ids=="":
                Item_ids=str(pk)
            else:
                Item_ids=Item_ids+"|"+str(pk)
            response.set_cookie('Item_ids', Item_ids)
        else:
            response.set_cookie('Item_ids', pk)

        Item=Items.objects.get(id=pk)
        messages.info(request, Item.name + ' added to cart successfully!')
        return response
    else:
        return redirect('login')


def full_view(request,pk):
    Item = Items.objects.filter(id=pk)
    return render(request,"full_view.html",{'menuitem':Item})

@login_required(login_url='login')
def cart(request):
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        counter=Item_ids.split('|')
        Item_count_in_cart=len(set(counter))
    else:
        Item_count_in_cart=0

    # fetching item details from db whose id is present in cookie
    Item=None
    total=0
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        if Item_ids != "":
            Item_id_in_cart=Item_ids.split('|')
            Item=Items.objects.all().filter(id__in = Item_id_in_cart)

            #for total price shown in cart
            for p in Item:
                total=total+p.price
    return render(request,'cart.html',{'menuitem':Item,'total':total,'Item_count_in_cart':Item_count_in_cart})

@login_required(login_url='login')
def remove_cart(request,pk):
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        counter=Item_ids.split('|')
        Item_count_in_cart=len(set(counter))
    else:
        Item_count_in_cart=0

    # removing item id from cookie
    total=0
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        Item_id_in_cart=Item_ids.split('|')
        Item_id_in_cart=list(set(Item_id_in_cart))
        Item_id_in_cart.remove(str(pk))
        Item=Items.objects.all().filter(id__in = Item_id_in_cart)
        #for total price shown in cart after removing item
        for p in Item:
            total=total+p.price

        #  for update coookie value after removing item id in cart
        value=""
        for i in range(len(Item_id_in_cart)):
            if i==0:
                value=value+Item_id_in_cart[0]
            else:
                value=value+"|"+Item_id_in_cart[i]
        response = render(request, 'cart.html',{'menuitem':Item,'total':total,'Item_count_in_cart':Item_count_in_cart})
        if value=="":
            response.delete_cookie('Item_ids')
        response.set_cookie('Item_ids',value)
        return response

@login_required(login_url='login')
def place_order(request):
    Item_in_cart=False
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        if Item_ids != "":
            Item_in_cart=True
    #for counter in cart
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        counter=Item_ids.split('|')
        Item_count_in_cart=len(set(counter))
    else:
        Item_count_in_cart=0

    placeorderForm = forms.PlaceOrderForm()
    if request.method == 'POST':
        placeorderForm = forms.PlaceOrderForm(request.POST)
        if placeorderForm.is_valid():
            email = placeorderForm.cleaned_data['Email']
            mobile=placeorderForm.cleaned_data['Mobile']
            address = placeorderForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of item from db
            total=0
            if 'Item_ids' in request.COOKIES:
                Item_ids = request.COOKIES['Item_ids']
                if Item_ids != "":
                    Item_id_in_cart=Item_ids.split('|')
                    Item1=Items.objects.all().filter(id__in = Item_id_in_cart)
                    for p in Item1:
                        total=total+p.price
            name = request.POST.get('cash')
            print(name)
            if name == 'Cash On Delivery':
                response = HttpResponseRedirect('payment_success')
                response.set_cookie('email',email)
                response.set_cookie('mobile',mobile)
                response.set_cookie('address',address)
            else:
                response = render(request, 'payment.html',{'total':total})
                response.set_cookie('email',email)
                response.set_cookie('mobile',mobile)
                response.set_cookie('address',address)
            return response
    return render(request,'place_order.html',{'placeorderForm':placeorderForm,'Item_in_cart':Item_in_cart,'Item_count_in_cart':Item_count_in_cart})


@login_required(login_url='login')
def payment_success(request):
    customer=Customer.objects.get(user_id=request.user.id)
    Itemss=[]
    email=None
    mobile=None
    address=None
    if 'Item_ids' in request.COOKIES:
        Item_ids = request.COOKIES['Item_ids']
        if Item_ids != "":
            Item_id_in_cart=Item_ids.split('|')
            Itemss=Items.objects.all().filter(id__in = Item_id_in_cart)
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']
    for item in Itemss:
        Order.objects.get_or_create(customer=customer,item=item,status='Pending',email=email,mobile=mobile,address=address)
    response = render(request,'payment_success.html')
    response.delete_cookie('Item_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response
      

@login_required(login_url='login')
def my_order(request):
    customer=Customer.objects.get(user_id=request.user.id)
    orders=Order.objects.all().filter(customer_id = customer)
    ordered_item=[]
    total =0
    address = ''
    status = ''
    for order in orders:
        ordered_items=Items.objects.all().filter(id=order.item.id)
        ordered_item.append(ordered_items)
        address = order.address
        status = order.status
        for item in ordered_items:
            total = total + item.price
    return render(request,'my_order.html',{'data':zip(ordered_item,orders),'addreses':address,'status':status,'total':total})

@login_required(login_url='login')
def cancel_order_view(request):
    total = 0
    amount = 0
    customer = Customer.objects.get(user_id = request.user.id)
    orders= Order.objects.all().filter(customer_id = customer)
    ordered_items=[]
    for order in orders:
        ordered_item = Items.objects.all().filter(id = order.item.id)
        ordered_items.append(ordered_item)
        for i in ordered_item:
            amount = total+i.price
            amt = amount*10/100
            total = amount-amt
    orders.delete()
    return render(request,'cancel_order.html',{'total':total})


@login_required(login_url='login')
def my_profile(request):
    customer=Customer.objects.get(user_id=request.user.id)
    return render(request,'my_profile.html',{'customer':customer})

@login_required(login_url='login')
def edit_profile_view(request):
    user = request.user
    customer=Customer.objects.get(user_id=request.user.id)
    user=User.objects.get(id=customer.user_id)
    userForm=CustomerUserForm(instance=user)
    customerForm=CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CustomerUserForm(request.POST,instance=user)
        customerForm=CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save(commit=False)
            raw_password = userForm.cleaned_data['password']
            user.set_password(raw_password)
            user.save()
            login(request,user)
            customerForm.save()
            return HttpResponseRedirect('my_profile')
    return render(request,'edit_profile.html',context=mydict)


def aboutus(request):
    return render(request,'aboutus.html')
