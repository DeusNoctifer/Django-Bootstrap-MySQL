from django.db import models

class Productos(models.Model):
    Nombre = models.CharField(max_length=45)
    Cantidad = models.SmallIntegerField()
    ValorVenta = models.IntegerField()
    Descripcion = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'productos'
        
    def categorias(self):
        return Categorias.objects.filter(
            id__in=ProductosCategoria.objects.filter(
                Productos=self
            ).values_list('Categoria_id', flat=True)
        ).distinct()

class Categorias(models.Model):
    Nombre = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class ProductosCategoria(models.Model):
    Productos = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'productoscategoria'
        unique_together = ('Productos', 'Categoria')  # Corregido para que coincida con los nombres de campos