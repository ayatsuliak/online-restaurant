from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import OrderForm
from .models import Order


@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                form.save_m2m()
                messages.success(request,
                                 f'Order #{order.id} successfully created!')
                return redirect('menu:menu_list')
        except ValidationError as e:
            form.add_error(None, e.message)
            messages.error(request, 'Please correct the form errors below.')
        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")
            form = OrderForm(request.POST)
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})
