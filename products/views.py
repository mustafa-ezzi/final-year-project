from django.shortcuts import get_object_or_404, render, redirect
from .models import Product


# ---------------- INDEX (SHOW DATA) ----------------
def index(request):
    data = Product.objects.all()
    context = {"data": data}
    return render(request, "admin.html", context)


def home(request):
    sections = [
        {
            "id": "mens-wear",
            "title": "MEN'S WEAR",
            "products": Product.objects.filter(category__iexact="Men"),
        },
        {
            "id": "womens-wear",
            "title": "WOMEN'S WEAR",
            "products": Product.objects.filter(category__iexact="Women"),
        },
        {
            "id": "kids-wear",
            "title": "KIDS WEAR",
            "products": Product.objects.filter(category__iexact="Kids"),
        },
    ]
    return render(request, "index.html", {"sections": sections})


# ---------------- INSERT ----------------
def insertData(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        badge = request.POST.get("badge", "").strip()  # avoid None
        category = request.POST.get("category")  # ← must come from form
        image = request.FILES.get("image")

        if not category or category not in dict(Product.CATEGORY_CHOICES):
            category = "Men"  # fallback

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            badge=badge,
            category=category,  # ← this was missing!
            image=image,
        )
        return redirect("index")

    # GET → show form
    return render(request, "insert.html", {"categories": Product.CATEGORY_CHOICES})


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
        return redirect("index")

    context = {"product": product}
    return render(request, "update.html", context)


# ---------------- DELETE ----------------
def deleteData(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("index")


def viewProduct(request, id):
    product = get_object_or_404(Product, id=id)

    context = {"product": product}
    return render(request, "view.html", context)
