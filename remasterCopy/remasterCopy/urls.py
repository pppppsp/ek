"""
URL configuration for remasterCopy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views 


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views


urlpatterns = [
    path('', views.LayoutView.main, name='home'),
    path('where/', views.LayoutView.whereus, name='where'),
    path('catalog/<str:order>/<int:filter>', views.LayoutView.catalog, name='catalog'),
    path('catalog/<int:id>', views.LayoutView.product_detail, name='product_detail'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/registration/', views.LayoutView.registration, name='registration'),
    path('cart_add/<int:id>', views.LayoutView.cart_add, name='cart_add'),
    path('cart_sub/<int:id>', views.LayoutView.cart_sub, name='cart_sub'),
    path('cart', views.LayoutView.cart, name='cart'),
    path('orders', views.LayoutView.orders, name='orders'),
    path('delete_order/<int:id>', views.LayoutView.delete_order, name="delete_order"),
    path('delete_order_ok/<int:id>', views.LayoutView.delete_order_ok, name="delete_order_ok"),
    path('create_order', views.LayoutView.create_order, name='create_order'),
    path('delete_order/<int:id>', views.LayoutView.delete_order, name='delete_order'),
    path('delete_order_ok/<int:id>', views.LayoutView.delete_order_ok, name='delete_order_ok'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

