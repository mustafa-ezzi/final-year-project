from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductImage


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
        # Get data once to keep it dry
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        badge = request.POST.get("badge", "").strip()
        category = request.POST.get("category", "Men")
        image = request.FILES.get("image")

        # Create the main product
        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            badge=badge,
            category=category,
            image=image,
        )

        # Handle the gallery
        gallery_images = request.FILES.getlist("gallery")
        for img in gallery_images[:4]:
            ProductImage.objects.create(product=product, image=img)

        return redirect("index")

    return render(request, "insert.html", {"categories": Product.CATEGORY_CHOICES})


# ---------------- UPDATE ----------------
def updateData(request, id):
    # Use prefetch_related if you want to be efficient
    product = get_object_or_404(Product, id=id)
    # Get all existing gallery images for this product
    gallery_images = product.images.all()

    if request.method == "POST":
        # ... (your existing field update logic) ...

        # Update Gallery
        new_gallery = request.FILES.getlist("gallery")
        if new_gallery:
            product.images.all().delete()  # Clears old, adds new
            for img in new_gallery[:4]:
                ProductImage.objects.create(product=product, image=img)

        product.save()
        return redirect("index")

    # Pass 'gallery' to the context
    context = {
        "d": product,
        "gallery": gallery_images,
        "categories": Product.CATEGORY_CHOICES,
    }
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
