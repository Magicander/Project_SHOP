from rest_framework import serializers
from .models import Product, Brand, Category, SIZES, FABRIC_TYPES, GENDER, COLORS
from django.contrib.auth.models import User

def validate_letters(value):
    clean_value = value.replace(" ", "")
    if not clean_value.isalpha():
        raise serializers.ValidationError("Pole może zawierać tylko litery!")
    return value

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, validators=[validate_letters])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock_count = serializers.IntegerField(default=1)
    sku = serializers.CharField(read_only=True)
    size = serializers.ChoiceField(choices=SIZES, default='M')
    fabric = serializers.ChoiceField(choices=FABRIC_TYPES, default='C')
    gender = serializers.ChoiceField(choices=GENDER, default='N')
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock_count = validated_data.get('stock_count', instance.stock_count)
        instance.size = validated_data.get('size', instance.size)
        instance.fabric = validated_data.get('fabric', instance.fabric)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.category = validated_data.get('category', instance.category)

        instance.save()
        return instance
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'website']

    def validate(self, data):
        name = data.get('name')
        country = data.get('country')
        if name and not name[0].isupper():
             raise serializers.ValidationError(
                {"name": "Nazwa marki musi zaczynać się z wielkiej litery!"}
            )
        if country:
            if len(country) != 2:
                raise serializers.ValidationError(
                    {"country": "Kod kraju musi mieć dokładnie 2 znaki (np. PL, US)."}
                )
            if not country.isupper():
                raise serializers.ValidationError(
                    {"country": "Kod kraju musi być napisany wielkimi literami."}
                )

        return data

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_letters])
    class Meta:
        model = Category
        fields = '__all__'