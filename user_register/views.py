from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm  # Make sure forms.py exists


# ---------- REGISTER ----------
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")  # new
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        delivery_type = request.POST.get("delivery_type")
        address = request.POST.get("address")

        # REQUIRED CHECK
        if not first_name or not phone_number or not delivery_type:
            messages.error(request, "Name, Phone number, and Delivery type are required")
            return render(request, "register.html")

        if delivery_type == "home" and not address:
            messages.error(request, "Address is required for Home Delivery")
            return render(request, "register.html")

        # DUPLICATE CHECK
        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return render(request, "register.html")

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            delivery_type=delivery_type,
            address=address,
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")


# ---------- LOGIN ----------
def login(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        if not phone_number:
            messages.error(request, "Phone number is required")
            return render(request, "login.html")

        customer = Customer.objects.filter(phone_number=phone_number).first()

        if not customer:
            messages.error(request, "Customer not found")
            return render(request, "login.html")

        # SIMPLE SESSION LOGIN
        request.session["customer_id"] = customer.id
        request.session["customer_name"] = f"{customer.first_name} {customer.last_name}"

        messages.success(request, "Login successful")
        return redirect("index")  # replace 'index' with your homepage

    return render(request, "login.html")


# ---------- LOGOUT ----------
def logout(request):
    request.session.flush()
    return redirect("login")


# ---------- CUSTOMER CREATE (DYNAMIC FORM) ----------
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # after submission
    else:
        form = CustomerForm()
    return render(request, 'user_register/customer_form.html', {'form': form})
