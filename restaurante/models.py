# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    direccion_entrega = models.TextField()
    telefono = models.CharField(max_length=20)
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - Usuario- {self.usuario.username}- Dirección - {self.direccion_entrega} - Telefono {self.telefono}- Notas del pedido- {self.notas}"
    
    def calcular_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total = total
        self.save()
        return total
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"


class Usuarios(models.Model):
    correo = models.CharField(verbose_name='correo',max_length=90)
    password=models.CharField(verbose_name='password',max_length=10)
    
    
    def __str__(self):
        return f'Correo del Cliente: {self.correo} Password: {self.password}'