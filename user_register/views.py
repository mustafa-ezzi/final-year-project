from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer


# ---------- REGISTER ----------
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        if not name or not email or not phone_number:
            messages.error(request, "All fields are required")
            return render(request, "register.html")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "register.html")

        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return render(request, "register.html")

        Customer.objects.create(
            name=name,
            email=email,
            phone_number=phone_number
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")


# ---------- LOGIN ----------
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        if not email and not phone_number:
            messages.error(request, "Email or Phone number required")
            return render(request, "login.html")

        user = None
        if email:
            user = Customer.objects.filter(email=email).first()
        elif phone_number:
            user = Customer.objects.filter(phone_number=phone_number).first()

        if not user:
            messages.error(request, "User not found")
            return render(request, "login.html")

        # simple session
        request.session["customer_id"] = user.id
        request.session["customer_name"] = user.name

        messages.success(request, "Login successful")
        return redirect("index")

    return render(request, "login.html")


# ---------- LOGOUT ----------
def logout(request):
    request.session.flush()
    return redirect("login")
