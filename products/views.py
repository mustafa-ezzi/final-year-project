from django.shortcuts import get_object_or_404, render, redirect
from .models import Product

# ---------------- INDEX (SHOW DATA) ----------------
def index(request):
    data = Product.objects.all()
    context = {'data': data}
    return render(request, 'admin.html', context)


# ---------------- INSERT ----------------
def insertData(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        badge = request.POST.get("badge")
        image = request.FILES.get("image")

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            badge=badge,
            image=image
        )
        return redirect('index')

    # return render(request, 'insert.html')


# ---------------- UPDATE ----------------
def updateData(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.badge = request.POST.get("badge")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return redirect('index')

    context = {'product': product}
    return render(request, 'update.html', context)


# ---------------- DELETE ----------------
def deleteData(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('index')
