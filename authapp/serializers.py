from rest_framework import serializers

from products.models import Product

class ProductsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, product):
        request=self.context.get('request')
        image_url = product.image.url 
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        fileds = ("id", "name", "short_description", "price", "image")
        fields = '__all__'
