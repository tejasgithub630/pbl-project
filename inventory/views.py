from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Product, Stock, Sale, Purchase
from .forms import ProductForm, SaleForm, PurchaseForm

def dashboard(request):
    products = Product.objects.all()
    low_stock_products = [p for p in products if p.is_low_stock]
    total_products = products.count()
    total_stock_value = sum(p.current_stock * p.price for p in products)
    
    # Get recent sales and purchases
    recent_sales = Sale.objects.all().order_by('-date')[:5]
    recent_purchases = Purchase.objects.all().order_by('-date')[:5]
    
    context = {
        'total_products': total_products,
        'total_stock_value': total_stock_value,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'recent_purchases': recent_purchases,
    }
    return render(request, 'inventory/dashboard.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stock = Stock.objects.get_or_create(product=product)[0]
    sales = Sale.objects.filter(product=product).order_by('-date')[:10]
    purchases = Purchase.objects.filter(product=product).order_by('-date')[:10]
    
    context = {
        'product': product,
        'stock': stock,
        'sales': sales,
        'purchases': purchases,
    }
    return render(request, 'inventory/product_detail.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            Stock.objects.create(product=product, quantity=0)
            messages.success(request, 'Product created successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Create'})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Edit'})

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()
            messages.success(request, 'Sale recorded successfully!')
            return redirect('product_detail', pk=sale.product.pk)
    else:
        form = SaleForm()
    return render(request, 'inventory/sale_form.html', {'form': form})

def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            messages.success(request, 'Purchase recorded successfully!')
            return redirect('product_detail', pk=purchase.product.pk)
    else:
        form = PurchaseForm()
    return render(request, 'inventory/purchase_form.html', {'form': form})
