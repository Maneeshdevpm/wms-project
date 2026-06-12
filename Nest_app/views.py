from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count

from .models import Product, StockTransaction
from .forms import ProductForm


# ---------------- DASHBOARD ----------------
@login_required
def index(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    total_products = products.count()
    total_stock = products.aggregate(Sum('quantity'))['quantity__sum'] or 0
    low_stock = Product.objects.filter(quantity__lt=10)

    recent_transactions = StockTransaction.objects.all().order_by('-date')[:5]

    return render(request, 'dashboard.html', {
        'products': products,
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'recent_transactions': recent_transactions
    })


# ---------------- PRODUCT CRUD ----------------
@login_required
def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_product.html', {'form': form})


@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_product.html', {'form': form})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('index')


# ---------------- STOCK IN / OUT ----------------
@login_required
def stock_transaction(request):

    if request.method == "POST":

        product_id = request.POST.get("product")
        transaction_type = request.POST.get("transaction_type")
        quantity = int(request.POST.get("quantity"))

        product = get_object_or_404(Product, id=product_id)

        if transaction_type == "IN":
            product.quantity += quantity

        elif transaction_type == "OUT":
            if product.quantity < quantity:
                return render(request, "error.html", {
                    "message": "Not enough stock!"
                })
            product.quantity -= quantity

        product.save()

        StockTransaction.objects.create(
            product=product,
            transaction_type=transaction_type,
            quantity=quantity
        )

        return redirect("transactions")

    products = Product.objects.all()

    return render(request, "stock_transaction.html", {
        "products": products
    })


# ---------------- TRANSACTIONS ----------------
@login_required
def transactions(request):
    transactions = StockTransaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {
        'transactions': transactions
    })


# ---------------- CATEGORY REPORT ----------------
@login_required
def category_report(request):

    categories = Product.objects.values('category').annotate(
        product_count=Count('id')
    )

    return render(request, 'category_report.html', {
        'categories': categories
    })


# ---------------- AUTH ----------------
def login_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

    