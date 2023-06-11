from marshmallow_enum import EnumField

from models import Ekart, CartItems, WishList, Sizes, Category
from utilities.serializer import ma


class EkartSerializer(ma.SQLAlchemyAutoSchema):
    gender = EnumField(Ekart.Gender)

    class Meta:
        model = Ekart
        include_fk = True
        load_instance = True


class CartItemsSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItems
        include_fk = True
        load_instance = True


class WishListSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WishList
        include_fk = True
        load_instance = True


class SizeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sizes
        include_fk = True
        load_instance = True


class CategorySerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
