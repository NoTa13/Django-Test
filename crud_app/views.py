from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item

# Read (List)
class ItemListView(ListView):
    model = Item
    template_name = 'crud_app/item_list.html'

# Read (Detail)
class ItemDetailView(DetailView):
    model = Item
    template_name = 'crud_app/item_detail.html'

# Create
class ItemCreateView(CreateView):
    model = Item
    fields = ['title', 'description']
    template_name = 'crud_app/item_form.html'
    success_url = reverse_lazy('item_list')

# Update
class ItemUpdateView(UpdateView):
    model = Item
    fields = ['title', 'description']
    template_name = 'crud_app/item_form.html'
    success_url = reverse_lazy('item_list')

# Delete
class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'crud_app/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')