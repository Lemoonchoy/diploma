from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q

from .models import Tour, Favorite, CartItem, Payment
from .forms import CustomUserCreationForm, CommentForm, ProfileForm


@login_required
def add_to_favorites(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, tour=tour)
    if created:
        messages.success(request, f'Тур «{tour.title}» добавлен в избранное!')
    else:
        favorite.delete()
        messages.info(request, f'Тур «{tour.title}» удалено из избранного.')

    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('tour')
    return render(request, 'voyage/favorites.html', {'favorites': favorites})


@login_required
def remove_from_favorites(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    favorite = Favorite.objects.filter(user=request.user, tour=tour).first()
    if favorite:
        favorite.delete()
        messages.success(request, f'Тур «{tour.title}» удалён из избранного!')
    else:
        messages.info(request, f'Тура «{tour.title}» нет в избранном.')
    return redirect('favorites')


@login_required
def profile_view(request):
    profile = request.user.profile
    favorites = Favorite.objects.filter(user=request.user).select_related('tour')

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "voyage/profile.html", {
        "form": form,
        "profile": profile,
        'favorites': favorites,
    })


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.tour.price * item.quantity for item in cart_items)
    total_count = sum(item.quantity for item in cart_items)

    return render(request, "voyage/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_count": total_count,
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'voyage/register.html', {'form': form})


def index(request):
    tours = Tour.objects.all()

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('tour_id', flat=True)

    return render(request, 'voyage/index.html', {'tours': tours, 'favorite_ids': list(favorite_ids)})


def catalog_view(request):
    category_slug = request.GET.get('category')
    continent_slug = request.GET.get('continent')
    query = request.GET.get('q')

    tours = Tour.objects.all().order_by('-id')

    if category_slug:
        tours = tours.filter(category__slug=category_slug)

    if continent_slug:
        tours = tours.filter(continent=continent_slug)

    if query:
        tours = tours.filter(
            Q(title__icontains=query) |
            Q(country__icontains=query) |
            Q(slogan__icontains=query)
        )

    paginator = Paginator(tours, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('tour_id', flat=True)

    return render(request, 'voyage/catalog.html',
                  {'page_obj': page_obj,
                   'current_category': category_slug,
                   'current_continent': continent_slug,
                   'favorites': favorites,
                   'query': query
                   })


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('tour_id', flat=True)

    comments = tour.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.tour = tour
                comment.save()
                messages.success(request, "Комментарий добавлен!")
                return redirect('tour_detail', pk=tour.pk)
        else:
            messages.error(request, "Нужно войти, чтобы оставлять комментарии!")

    return render(request, 'voyage/detail.html',
                  {'tour': tour,
                   'favorites': favorites,
                   'comments': comments,
                   'form': form
                   })


@login_required()
def add_to_cart(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, tour=tour)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{tour.title} добавлен в корзину")
    return redirect(request.META.get("HTTP_REFERER", "index"))


@login_required()
def remove_from_cart(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    CartItem.objects.filter(user=request.user, tour=tour).delete()
    messages.warning(request, f"{tour.title} удалён из корзины")
    return redirect("cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    for item in cart_items:
        payment, created = Payment.objects.get_or_create(
            user=request.user,
            tour=item.tour,
            defaults={"amount": item.tour.price * item.quantity, "status": "paid"}
        )
        if not created:
            # если уже существует, увеличим сумму
            payment.amount += item.tour.price * item.quantity
            payment.status = "paid"
            payment.save()

    cart_items.delete()

    return redirect("tickets")


@login_required
def tickets_view(request):
    tickets = Payment.objects.filter(user=request.user, status="paid").select_related("tour")
    return render(request, "voyage/tickets.html", {"tickets": tickets})
