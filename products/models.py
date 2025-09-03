from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=150, null=False)
    url = models.URLField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Список магазинов"
        ordering = ("name",)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)
    shops = models.ManyToManyField(Shop, related_name="categories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Список категорий"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"
        ordering = ("name",)


class ProductInfo(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)
    quantity = models.IntegerField(null=False)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    price_rrc = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="infos")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="infos")

    def __str__(self):
        return f"{self.product} {self.shop}"

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Список информации о продуктах"
        ordering = ("product",)


class Parameter(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Список параметров"
        ordering = ("name",)


class ProductParameter(models.Model):
    value = models.CharField(max_length=150, null=False)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="product_parameters")
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name="product_parameters")

    def __str__(self):
        return f"{self.product_info} {self.parameter}"

    class Meta:
        verbose_name = "Параметр продукта"
        verbose_name_plural = "Список параметров продуктов"
        ordering = ("product_info",)
