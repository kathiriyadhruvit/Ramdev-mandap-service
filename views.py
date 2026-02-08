from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student,Contact, Product, ProductVariant, Cart, Order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# HOME PAGE
def homepage(request):
    data = {
        'name': 'Dhulo',
        'pin': 362020,
        'city': 'surat'
    }
    return render(request, "index.html", {'data': data})

def index(request):
    products = Product.objects.all()
    if not request.session.get('is_login'):
        return redirect('/log')
    return render(request, 'index.html', {'products': products,'id':request.session.get('id'),'email':request.session.get('email')})
   



def about(request):
    if not request.session.get('is_login'):
        return redirect('/log')
    return render(request, "about.html")


def gallery(request):
    if not request.session.get('is_login'):
        return redirect('/log')
    return render(request, "gallery.html")


def services(request):
    if not request.session.get('is_login'):
        return redirect('/log')
    return render(request, "services.html")


def contact(request):
    if not request.session.get('is_login'):
        return redirect('/log')
    return render(request, "contact.html")


# EVEN / ODD FORM
def form(request):
    result = ""
    try:
        if request.method == "POST":
            n1 = int(request.POST.get('username'))

            if n1 % 2 == 0:
                result = "Even Number"
            else:
                result = "Odd Number"
    except:
        result = "Invalid Input"

    return render(request, "form.html", {'output': result})


# CALCULATOR
def calculator(request):
    c = ""
    try:
        if request.method == "POST":
            n1 = int(request.POST.get('v1'))
            n2 = int(request.POST.get('v2'))
            opr = request.POST.get('opr')

            if opr == "+":
                c = n1 + n2
            elif opr == "-":
                c = n1 - n2
            elif opr == "*":
                c = n1 * n2
            elif opr == "/":
                c = n1 / n2
    except:
        c = "Error"

    return render(request, "calculator.html", {"output": c})


# CREATE STUDENT
def form1(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")

        Student.objects.create(
            name=name,
            age=age
        )

        return render(request, "form1.html", {"msg": "Record Saved Successfully!"})

    return render(request, "form1.html")
# STUDENT LIST
def student_list(request):
    student = Student.objects.all()
    return render(request, 'student_list.html', {'student': student})


# UPDATE
def student_update(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.age = request.POST.get("age")
        student.save()
        return redirect('student_list')

    return render(request, 'student_update.html', {'student': student})


# DELETE
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')

# CONTACT FORM (INSERT)
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        return render(request, "contact.html", {
            "msg": "Record Saved Successfully!"
        })

    return render(request, "contact.html")


# CONTACT LIST
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contact_list.html', {
        'contacts': contacts
    })


# CONTACT UPDATE
def contact_update(request, id):
    contacts=get_object_or_404(Contact,id=id)
    if request.method == "POST":
        contacts.name = request.POST.get("name")
        contacts.email = request.POST.get("email")
        contacts.phone = request.POST.get("phone")
        contacts.message = request.POST.get("message")

        contacts.save()
        return redirect('contact_list')

    return render(request, 'contact_update.html', {
        'contacts': contacts
    })


# CONTACT DELETE
def contact_delete(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect('contact_list')
# sign_up form
def reg(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        if password!=confirmpassword:
            return HttpResponse("Areyou not validate confirm password")
        else:
            myuser=User.objects.create_user(username,email,password)
            myuser.save()
            return redirect('/log')
    return render(request,'signup.html')
#login form
def log(request):
    msg=""
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['id']=user.id
            request.session['email']=user.email
            request.session['is_login']=True
            return redirect('/index/')
        else:
            msg="Invalid username and password!!!"
    return render(request,'log.html',{'msg':msg})
#logout
def log_out(request):
    logout(request)
    # request.session.session_expiry(10)
    return redirect('/log/')



#signup list
def order_list(request):
    users = Order.objects.all()
    return render(request, 'order_list.html', {'users': users})

#order update
def order_update(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":
        order.varient = request.POST.get('varient')
        order.name = request.POST.get('name')
        order.mobile = request.POST.get('mobile')
        order.address = request.POST.get('address')
        order.save()

        return redirect('order_list')

    return render(request, 'order_update.html', {'order': order})

#signup delete
def order_delete(request, id):
    user = get_object_or_404(Order, id=id)
    user.delete()
    return redirect('/order/list')
#cart===================cart========================
# ----------------------
# Product List Page (Client side)
# ----------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# ----------------------
# Add to Cart (with Variant)
# ----------------------
def add_to_cart(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    Cart.objects.create(variant=variant, quantity=1)
    return redirect('cart')



# ----------------------
# Cart Page (Form open for order)
# ----------------------
def cart(request):
    items = Cart.objects.all()

    total = 0
    for i in items:
        total += i.variant.price * i.quantity

    print("Cart items:", items)
    print("Total:", total)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
def my_orders(request):
    orders = Order.objects.all()

    order_total = 0
    for o in orders:
        order_total += o.variant.price * o.quantity

    return render(request, 'orders.html', {
        'orders': orders,
        'order_total': order_total
    })





# ----------------------
# Update Cart Quantity
# ----------------------
def update_cart(request, cart_id):
    if request.method == 'POST':
        cart_item = Cart.objects.get(id=cart_id)
        new_qty = int(request.POST['quantity'])
        if new_qty > 0:
            cart_item.quantity = new_qty
            cart_item.save()
    return redirect('cart')


# ----------------------
# Delete Cart Item
# ----------------------
def delete_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect('cart')


# ----------------------
# Place Order
# ----------------------
def place_order(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)

    # Create Order
    Order.objects.create(
        variant=cart_item.variant,
        name=request.POST['name'],
        mobile=request.POST['mobile'],
        address=request.POST['address'],
        quantity=cart_item.quantity,
        status='Pending'
    )

    # Remove item from Cart
    cart_item.delete()
    return redirect('orders')


# ----------------------
# Orders List (Client side)
# ----------------------
def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})

def fun(request):
    return HttpResponse("<h1>welcome to dhula</h1>")
def admin(request):
    users = Order.objects.all()
    if not request.session.get('is_login'):
        return redirect('/log')
    
    return render(request, 'admin.html', {'users': users})
