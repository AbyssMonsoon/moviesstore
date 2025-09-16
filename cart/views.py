from django.shortcuts import render
from .models import Order, Item
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie

from .utils import calculate_cart_total
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    # enforce quantity does not exceed amount_left when set
    qty = int(request.POST['quantity'])
    movie = Movie.objects.get(id=id)
    amount_left = getattr(movie, 'amount_left', None)
    if amount_left is not None:
        try:
            amount_left = int(amount_left)
        except Exception:
            amount_left = None
    if amount_left is not None:
        if amount_left <= 0:
            # can't add out of stock
            return redirect('cart.index')
        if qty > amount_left:
            qty = amount_left
    cart[id] = str(qty)
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = int(cart[str(movie.id)])
        item.save()
        # decrement stock if amount_left is set; use getattr to avoid errors
        amount_left = getattr(movie, 'amount_left', None)
        if amount_left is not None:
            try:
                new_amount = int(amount_left) - item.quantity
            except Exception:
                new_amount = None
            if new_amount is not None:
                if new_amount < 0:
                    new_amount = 0
                movie.amount_left = new_amount
                movie.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})