from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer


# ---------- REGISTER ----------
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        address = request.POST.get("address")

        # REQUIRED CHECK
        if not name or not phone_number:
            messages.error(request, "Name and Phone number are required")
            return render(request, "register.html")

        # DUPLICATE CHECK
        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return render(request, "register.html")

        Customer.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
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
        request.session["customer_name"] = customer.name

        messages.success(request, "Login successful")
        return redirect("index")

    return render(request, "login.html")


# ---------- LOGOUT ----------
def logout(request):
    request.session.flush()
    return redirect("login")
