from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Category, Product


@login_required
def dashboard(request):
    counts = {
        "total_products": Product.objects.count(),
        "active_products": Product.objects.filter(is_active=True).count(),
        "inactive_products": Product.objects.filter(is_active=False).count(),
        "low_stock_products": Product.objects.filter(stock__lte=5).count(),
    }
    return render(request, "catalog/dashboard.html", counts)


@login_required
def product_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")

    products = Product.objects.select_related("category").order_by("-created_at")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    if category_id.isdigit():
        products = products.filter(category_id=category_id)
    if status == "active":
        products = products.filter(is_active=True)
    elif status == "inactive":
        products = products.filter(is_active=False)

    page_obj = Paginator(products, 8).get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "categories": Category.objects.order_by("name"),
        "query": query,
        "selected_category": category_id,
        "selected_status": status,
    }
    return render(request, "catalog/product_list.html", context)


@login_required
def product_form(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk is not None else None
    form = ProductForm(
        data=request.POST if request.method == "POST" else None,
        files=request.FILES if request.method == "POST" else None,
        instance=product,
    )
    if request.method == "POST" and form.is_valid():
        saved_product = form.save()
        action = "updated" if product else "added"
        messages.success(request, f"{saved_product.name} was {action}.")
        return redirect("product_list")
    return render(request, "catalog/product_form.html", {"form": form, "product": product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("product_list")
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])
    return render(request, "catalog/product_confirm_delete.html", {"product": product})
