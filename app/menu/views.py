from django.shortcuts import get_object_or_404, render

from .models import MenuItem


def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'menu/menu_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})
