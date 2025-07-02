from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido,Usuarios

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'disponible', 'fecha_creacion']
    list_filter = ['categoria', 'disponible', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'disponible']
    ordering = ['-fecha_creacion']

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']
    
    def subtotal(self, obj):
        return obj.subtotal() if obj.id else 0
    subtotal.short_description = 'Subtotal'

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'estado', 'total', 'telefono']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['usuario__username', 'usuario__email', 'telefono']
    list_editable = ['estado']
    readonly_fields = ['fecha_pedido', 'total']
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('usuario', 'fecha_pedido', 'estado', 'total')
        }),
        ('Información de Entrega', {
            'fields': ('direccion_entrega', 'telefono', 'notas')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Recalcular total cuando se guarde
        obj.calcular_total()

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido__fecha_pedido', 'producto__categoria']
    search_fields = ['pedido__id', 'producto__nombre']
    
    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'

# Personalizar el header del admin
admin.site.site_header = "Administración del Restaurante"
admin.site.site_title = "Restaurante Admin"
admin.site.index_title = "Panel de Administración"

admin.site.register(Usuarios)