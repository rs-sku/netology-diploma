import yaml
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.permissions import IsShopPermission
from products.serializers import ImportSerializer, ProductSerializer


class ImportView(APIView):
    def get_permissions(self) -> list:
        return [IsAuthenticated(), IsShopPermission()]

    def post(self, request: Request) -> Response:
        file = request.FILES.get("file")
        if not file:
            return Response(data={"error": "No file provided"}, status=400)
        file = file.read().decode("utf-8")

        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError:
            return Response(data={"error": "Invalid file format"}, status=400)

        serializer = ImportSerializer()

        try:
            shop_object = serializer.create_shop(data["shop"])
            for category in data["categories"]:
                serializer.create_category(category["id"], category["name"])
            for product in data["goods"]:
                try:
                    product_object = serializer.create_product(
                        product["id"], product["name"], product["category"]
                    )
                    product_info_object = serializer.create_product_info(
                        product["model"],
                        product["quantity"],
                        product["price"],
                        product["price_rrc"],
                        product_object,
                        shop_object,
                    )
                    for parameter_name, parameter_value in product[
                        "parameters"
                    ].items():
                        parameter_object = serializer.create_parameter(parameter_name)
                        serializer.create_product_parameter(
                            parameter_value, parameter_object, product_info_object
                        )
                except IntegrityError:
                    continue

        except (KeyError, TypeError):
            return Response(data={"error": "Invalid file format"}, status=400)

        return Response(data={"message": "File imported successfully"}, status=201)


class ListProductsView(APIView):
    def get(self, request: Request) -> Response:
        queryset = Product.objects.prefetch_related(
            "infos", "infos__product_parameters"
        ).all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            product = Product.objects.prefetch_related(
                "infos", "infos__product_parameters"
            ).get(id=pk)
        except Product.DoesNotExist:
            return Response(data={"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
