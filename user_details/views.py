from django.shortcuts import render,redirect
import csv
import mysql.connector
from user_details.models import user_details,checkout
from user_details.models import login, products,cart_contents
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required


'''from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm

'''
# Create your views here.

i=User.objects.get(username='supreeth')
print (i)


print(i)
username1=User.username
#print(username1)
#print(user.username)

#print(username1)
def user(request):
	if request.method=="POST":
		global username1
		username1=request.POST["Username"]
		first_name=request.POST["first_name"]
		last_name=request.POST["last_name"]
		email=request.POST["email"]
		phone=request.POST["phone"]
		passw=request.POST["password"]
		passwordConfirm=request.POST["passwordConfirm"]
		if (passw!=passwordConfirm):
			return render(request,'register.html')
		#print(user_details_login.objects.all())
		try:
			u=user_details.objects.get(username=username1)
		except:
			u=None
		if(u):
			return render(request,'register.html')
		else:
			tb=user_details()
			tb.username=username1
			tb.first_name=first_name
			tb.last_name=last_name
			tb.email=email
			tb.phone=phone
			tb.passw=passw
			tb.cpass=passwordConfirm
			tb.save()
			#print (tb.id)
			lo=login()
			lo.username=username1
			lo.password=passw
			lo.save()



		return render(request,'login.html')
	else:
		return render(request,'register.html')

def login2(request):
	return render(request, 'login2.html')


user_name=0
def login1(request):
	if request.method=="POST":
		p=products.objects.all()
		username2=request.POST["user"]
		username2 = username2.strip()
		password1=request.POST["password"]
		u = user_details.objects.filter(username=username2)
		print(u.values("passw"))
		user_name=username2
		for i in u.values("passw"):
			if i["passw"] == password1:
				print("here")
				print(username2)
				username1=username2
				return render(request,'homepage1.html',{'p':p})
		return render(request,'login.html')
	else:
		return render(request,'login.html')

def welcome(request):
	return render(request,'welcome.html')
"""
def index(request):
	global username1
	user=user_details.objects.filter(username=username1)
	return render(request,"index.html",{'c':user})
"""

@login_required
def homepage(request):


	p=products.objects.all()
	for i in p:
		print(i)
	return render(request,"homepage1.html" ,{'p':p})
@login_required
def product(request):
	if request.method=="POST":
		p_id=request.POST["pid"]
		p=products.objects.get(product_id=p_id)
		rel=products.objects.all()
		print(p.product_name,'pname')
		return render(request,'product.html',{'pdesc':p,'rel':rel})
@login_required
def cart(request):
	if request.method=="POST":
		user=request.user
		u=user.username
		print(u)
		c=cart_contents.objects.filter(username=u,status="cart")
		return render(request,'cart.html',{'c':c})
	else:
		user=request.user
		u=user.id
		c=cart_contents.objects.filter(username=u,status="cart")
		return render(request,'cart.html',{'c':c})

@login_required
def your_orders(request):
	if request.method=="POST":
		user=request.user
		u=user.id
		c=cart_contents.objects.filter(username=u,status="Ordered")
		return render(request,'your_orders.html',{'c':c})
	else:
		user=request.user
		u=user.id
		c=cart_contents.objects.filter(username=u,status="Ordered")
		return render(request,'your_orders.html',{'c':c})
@login_required
def add_to_cart(request):
	if request.method=="POST":
		user=request.user
		u=user.id
		p_id=request.POST['pid']
		p=products.objects.get(product_id=p_id)
		if cart_contents.objects.filter(product_id=p_id,username=u):
		#tb=cart_contents()
		#print(p.product_id,p.product_name)
			tb=cart_contents.objects.get(product_id=p_id,username=u)
			#tb.username=username1
			tb.product_id=p.product_id
			tb.product_type=p.product_type
			tb.product_name=p.product_name
			tb.product_desc=p.product_desc
			tb.product_price=p.product_price
			tb.product_pic=p.product_pic
			tb.status="cart"
			tb.quantity=tb.quantity+1
			tb.total=tb.quantity*int(tb.product_price)
			tb.save()
		else:
			tb=cart_contents()
			user=request.user
			u=user.id
			tb.username_id=u
			#tb.username=user.username
			#print(p.product_id,p.product_name)
			tb.product_id=p.product_id
			tb.product_type=p.product_type
			tb.product_name=p.product_name
			tb.product_desc=p.product_desc
			tb.product_price=p.product_price
			tb.product_pic=p.product_pic
			tb.status="cart"
			tb.quantity=1
			tb.total=int(tb.product_price)
			tb.save()
		return render(request,'product.html',{'pdesc':p})
@login_required
def check_out(request):
	user=request.user
	us=user.id
	c=cart_contents.objects.filter(username=us)
	to=0
	print(c)
	u=user_details.objects.filter(username=us)
	for i in c:
		to+=i.total
	return render(request,'checkout1.html',{'c':c ,"total":to,"user":u})
@login_required
def place_order(request):
	if request.method=="POST":
		first_name=request.POST['checkout_name']   
		last_name=request.POST['checkout_last_name']
		address=request.POST['checkout_address']
		locality=request.POST['checkout_address_2']
		city=request.POST['checkout_city']
		zipcode=request.POST['checkout_zipcode']
		province=request.POST['checkout_province']
		Phone=request.POST['checkout_phone']
		check_email=request.POST['checkout_email']
		#payment=request.POST['']
		tb=checkout()
		tb.first_name=first_name
		tb.last_name=last_name
		tb.address=address
		tb.locality=locality
		tb.city=city
		tb.zipcode=zipcode
		tb.province=province
		tb.Phone=Phone
		tb.check_email=check_email
		tb.save()
		#tb1=cart_contents()
		user=request.user
		u=user.id
		for i in cart_contents.objects.filter(username=u):
			i.status="Ordered"
			i.save()
		return render(request,'homepage1.html')
	else:
		return render(request,'checkout1.html')

'''
def logout(request):
	global username1
	username1=""
	return render(request,'welcome.html')
'''



'''
@login_required
def update(request):
	if request.method=="POST":
		#user=request.POST["username"]
		first=request.POST["first_name"]
		last=request.POST["last_name"]
		mail=request.POST["email"]
		passw=request.POST["password"]
		cpassw=request.POST["passwordConfirm"]
		if passw!=request.POST["passwordConfirm"]:
			return render(request,'account.html')
		det=user_details.objects.get(username=j)
		det.first_name=first
		det.last_name=last
		det.email=mail
		det.passw=passw
		det.cpass=cpassw
		det.save()
	user = user_details.objects.filter(username=j)
	context= {'details': user}
	print(username1)
	print(user)
	return render(request,"account.html",context)
'''

@login_required
def update_cart(request):
	if request.method=="POST":
		user=request.user
		us=user.id
		pr=request.POST["name1"]
		u=cart_contents.objects.get(username=us,product_name=pr)
		u.quantity=request.POST["quantity_input"]
		u.save()
		u.total=int(u.product_price)*int(u.quantity)
		u.save()
		user=request.user
		us=user.id
		c=cart_contents.objects.filter(username=us,status="cart")
		return render(request,'cart.html',{'c':c})

def glog(request):
	return render(request,'glogin.html')
	
'''

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "loginz.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')

    '''