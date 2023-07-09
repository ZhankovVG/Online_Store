from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib import messages


class Mixin:
    # Class Mixin
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context
    

class ProductView(Mixin, ListView):
    # Output Produckt
    model = Product
    queryset = Product.objects.filter(available=False)
    paginate_by = 4
      

class CategoryView(Mixin, ListView):
    # Product listing by category
    model = Product
    template_name = 'shop/product_list.html'
    
    def get_queryset(self):
        category = get_object_or_404(Category, url=self.kwargs['cat_slug'])
        return Product.objects.filter(category=category)
    
    
class ProductDetailView(Mixin, DetailView):
    # Full product description
    model = Product
    slug_field = 'url'
    template_name = 'shop/detail_list.html'
    
    
class SearchView(Mixin, ListView):
    # Search produccts
    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = Product.objects.filter(name__icontains=search_query)
        
        if not queryset.exists():
            messages.warning(self.request, f"Товар '{search_query}' не найден.")
        
        return queryset