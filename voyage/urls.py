from django.urls import path

from .views import catalog_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', catalog_view, name='catalog'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:tour_id>/', views.remove_from_cart, name='remove_from_cart'),

    path("checkout/", views.checkout, name="checkout"),

    path("tickets/", views.tickets_view, name="tickets"),

    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
    path("profile/", views.profile_view, name="profile"),
]
