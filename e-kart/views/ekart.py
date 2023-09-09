from http import HTTPStatus

from flask import views, request, jsonify
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Ekart, CartItems, WishList, Sizes, Category
from serializers import (
    EkartSerializer,
    CartItemsSerializer,
    WishListSerializer,
    SizeSerializer,
    CategorySerializer,
)
from utilities.database import db


def get_data_from(serializer, model, pk):
    data = model.query.get(pk)

    return serializer().dump(data)


class EkartView(views.MethodView):
    """
    Ekart View
    """

    model = Ekart
    serializer_class = EkartSerializer

    def get(self, *args, **kwargs):
        products = self.model.query.all()
        serializer = self.serializer_class(many=True)
        result = serializer.dump(products)

        for product in result:
            category = get_data_from(
                CategorySerializer, Category, product["category_id"]
            )
            size = get_data_from(SizeSerializer, Sizes, product["size_id"])
            product["size"] = size["size"]
            product["category"] = category["category"]

        return jsonify(result), HTTPStatus.OK

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class()
            product = serializer.load(request.json)
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            return (
                jsonify({"message": "Product already exists!"}),
                HTTPStatus.BAD_REQUEST,
            )

        return jsonify(serializer.dump(product)), HTTPStatus.OK


class EkartIDView(views.MethodView):
    """
    EkartIDView
    """

    model = Ekart
    serializer_class = EkartSerializer

    def get(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        serializer = self.serializer_class()

        result = serializer.dump(product)
        category = get_data_from(CategorySerializer, Category, result["category_id"])
        size = get_data_from(SizeSerializer, Sizes, result["size_id"])
        result["size"] = size["size"]
        result["category"] = category["category"]

        return jsonify(result), HTTPStatus.OK

    def put(self, *args, **kwargs):
        try:
            product = self.model.query.get(kwargs["id"])
            if not product:
                return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
            serializer = self.serializer_class()
            serializer.load(request.json, instance=product, partial=False)
            db.session.commit()

        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(product)), HTTPStatus.OK

    def patch(self, *args, **kwargs):
        try:
            product = self.model.query.get(kwargs["id"])
            if not product:
                return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
            serializer = self.serializer_class()
            serializer.load(request.json, instance=product, partial=True)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(product)), HTTPStatus.OK

    def delete(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        self.model.query.filter_by(id=kwargs["id"]).delete()
        db.session.commit()

        return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND


class CartItemsView(views.MethodView):
    """
    CartItems view
    """

    model = CartItems
    serializer_class = CartItemsSerializer

    def get(self, *args, **kwargs):
        products = self.model.query.all()
        serializer = self.serializer_class(many=True)
        result = serializer.dump(products)

        for product in result:
            item = get_data_from(EkartSerializer, Ekart, product["cart_item"])
            category = get_data_from(CategorySerializer, Category, item["category_id"])
            size = get_data_from(SizeSerializer, Sizes, item["size_id"])
            item["size"] = size["size"]
            item["category"] = category["category"]
            product["product"] = item

        return jsonify(result), HTTPStatus.OK

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class()
            product = serializer.load(request.json)
            db.session.add(product)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(product)), HTTPStatus.OK


class CartItemsIDView(views.MethodView):
    """
    CartItemsID view
    """

    model = CartItems
    serializer_class = CartItemsSerializer

    def get(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        serializer = self.serializer_class()
        result = serializer.dump(product)

        item = EkartSerializer().dump(Ekart.query.get(result["cart_item"]))

        category = get_data_from(CategorySerializer, Category, result["category_id"])
        size = get_data_from(SizeSerializer, Sizes, item["size_id"])
        item["size"] = size["size"]
        item["category"] = category["category"]
        result["product"] = item

        return jsonify(result), HTTPStatus.OK

    def put(self, *args, **kwargs):
        try:
            product = self.model.query.get(kwargs["id"])
            if not product:
                return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
            serializer = self.serializer_class()
            serializer.load(request.json, instance=product, partial=False)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(product)), HTTPStatus.OK

    def patch(self, *args, **kwargs):
        try:
            product = self.model.query.get(kwargs["id"])
            if not product:
                return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
            serializer = self.serializer_class()
            serializer.load(request.json, instance=product, partial=True)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(product)), HTTPStatus.OK

    def delete(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        self.model.query.filter_by(id=kwargs["id"]).delete()
        db.session.commit()

        return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND


class WishListView(views.MethodView):
    model = WishList
    serializer_class = WishListSerializer

    def get(self, *args, **kwargs):
        products = self.model.query.all()
        serializer = self.serializer_class(many=True)
        result = serializer.dump(products)

        for product in result:
            item = EkartSerializer().dump(Ekart.query.get(product["cart_item"]))
            product["product"] = item

        return jsonify(result), HTTPStatus.OK

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class()
            product = serializer.load(request.json)
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            return (
                jsonify({"message": "Item is already in the wishlist."}),
                HTTPStatus.BAD_REQUEST,
            )

        return jsonify(serializer.dump(product)), HTTPStatus.OK


class WishListIDView(views.MethodView):
    model = WishList
    serializer_class = WishListSerializer

    def get(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        serializer = self.serializer_class()
        result = serializer.dump(product)

        item = EkartSerializer().dump(Ekart.query.get(result["cart_item"]))
        result["product"] = item

        return jsonify(serializer.dump(product)), HTTPStatus.OK

    def delete(self, *args, **kwargs):
        product = self.model.query.get(kwargs["id"])
        if not product:
            return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND
        self.model.query.filter_by(id=kwargs["id"]).delete()
        db.session.commit()

        return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND


class SizesView(views.MethodView):
    model = Sizes
    serializer_class = SizeSerializer

    def get(self, *args, **kwargs):
        sizes = self.model.query.all()
        serializer = self.serializer_class(many=True)
        result = serializer.dump(sizes)

        return jsonify(serializer.dump(sizes)), HTTPStatus.OK

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class()
            sizes = serializer.load(request.json)
            db.session.add(sizes)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        return jsonify(serializer.dump(sizes)), HTTPStatus.OK


class CategoryView(views.MethodView):
    model = Category
    serializer_class = CategorySerializer

    def get(self, *args, **kwargs):
        sizes = self.model.query.all()
        serializer = self.serializer_class(many=True)

        return jsonify(serializer.dump(sizes)), HTTPStatus.OK

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class()
            sizes = serializer.load(request.json)
            db.session.add(sizes)
            db.session.commit()
        except IntegrityError:
            return (
                jsonify({"message": "Data duplication not allowed."}),
                HTTPStatus.BAD_REQUEST,
            )

        return jsonify(serializer.dump(sizes)), HTTPStatus.OK
