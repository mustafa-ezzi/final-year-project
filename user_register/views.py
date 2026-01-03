from django.shortcuts import render
from products.models import Product
from user_register import views
from user_register.models import Customer
# Create your views here.

def index(request):
    data = Product.objects.all()
    context = {'data': data}  # send to index.html
    return render(request, 'index.html', context)

def view(request):
    return render(request, 'view.html')

def insertData(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(name, email, password)
        query=Customer(name=name,email=email,password=password)
        query.save()
    return render(request, 'index.html')

def viewData(request):
    
    data=Customer.objects.all()
    context = {'data': data}
    return render(request, "view.html",context)

def updateData(request, id):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        edit = Customer.objects.get(id=id)
        edit.name = name
        edit.email = email
        edit.password = password
        edit.save()
        return viewData(request)
        
    d = Customer.objects.get(id=id)
    
    context = {'d': d}
    return render(request, "update.html", context)


def deletData(request,id):
    d =  Customer.objects.get(id=id)
    d.delete()
    return viewData(request)