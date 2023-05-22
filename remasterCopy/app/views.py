from django.contrib.auth.decorators import login_required
from app.forms import *
from django.shortcuts import render, redirect
from django.views import View
from app.models import*
from django.http import HttpResponseRedirect, HttpResponse

class LayoutView(View):
    
    # главная страница
    def main(req):
        products = Product.objects.all().filter(amount__gte=0).order_by('-id')[:5]
        return render(req, 'index.html', {'products':products})


    #где нас найти 
    def whereus(req):
        return render(req, 'pages/where.html')

    # каталог c товарами
    def catalog(req, order, filter):
        rows = Product.objects.all().order_by(order)
        if filter:
            rows = rows.filter(category__id=filter)
        category = Category.objects.all().order_by('name')
        if req.user.is_authenticated:
            for row in rows:
                cart = Cart.objects.filter(user=req.user, product=row).first()
                row.cart = cart.amount if cart else 0
        return render(req, 'pages/catalog.html', context={'products': rows, 'categories': category, 'order': order, 'filter': filter})


    # подробности товара
    def product_detail(req, id):
        row = Product.objects.get(pk=id)
        if req.user.is_authenticated:
            cart = Cart.objects.filter(user=req.user, product=row).first()
            row.cart = cart.amount if cart else 0
        return render(req, 'pages/prod_det.html', context={'product': row})


    # регистрация
    def registration(req):
        if req.method == 'POST':
            form = RegistrationForm(req.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = RegistrationForm()
        return render(req, 'registration/reg.html', context={'form': form})


    # корзина
    @login_required
    def cart(req):
        products = Cart.objects.all().filter(user=req.user)
        return render(req, 'pages/cart.html', context={'products': products})


    # добавление в корзину
    @login_required
    def cart_add(req, id):
        row = Cart.objects.all().filter(user=req.user, product=id)
        product = Product.objects.get(pk=id)
        if len(row):
            row = row[0]
            if row.amount >= product.amount:
                return HttpResponse("<span class='error-count'>Больше добавить нельзя! в корзине %s шт</span>" % row.amount)
            row.amount += 1
        else:
            row = Cart(user=req.user, product=product, amount=1)
        row.save()
        return HttpResponse("в корзине %s шт" % row.amount)


    # удаление из корзины
    @login_required
    def cart_sub(req, id):
        row = Cart.objects.all().filter(user=req.user, product=id)
        if len(row):
            row = row[0]
            if row.amount:
                row.amount -= 1
                row.save() if row.amount else row.delete()
                return HttpResponse("в корзине %s шт" % row.amount)
            return HttpResponse("<span class='error-count'>Товар в корзине отсутствует!</span>")


    # создание заказа
    @login_required
    def create_order(req):
        if req.method == 'POST':
            form = CreateOrderForm(req.POST)
            if req.user.check_password(req.POST['password']):
                order = Order(user=req.user)
                order.save()
                products = Cart.objects.all().filter(user=req.user)
                for p in products:
                    op = OrderProduct(order=order, product=p.product, amount=p.amount)
                    op.save()
                    p.delete()
                return HttpResponseRedirect('orders')
            else:
                form.add_error('password', 'Неверный пароль')
        else:
            form = CreateOrderForm()
        return render(req, 'pages/create_order.html', context={'form': form})


    # заказы
    @login_required
    def orders(req):
        orders = Order.objects.all().filter(user=req.user).order_by('-date_create')
        return render(req, 'pages/orders.html', context={'orders': orders})

    
    # удаление заказа
    @login_required
    def delete_order(req, id):
        order = Order.objects.get(pk=id)
        return render(req, 'pages/delete_order.html', context={'order': order})


    # подтверждение удаления
    @login_required
    def delete_order_ok(req, id):
        order = Order.objects.get(pk=id)
        order.delete()
        return HttpResponseRedirect('/orders')


