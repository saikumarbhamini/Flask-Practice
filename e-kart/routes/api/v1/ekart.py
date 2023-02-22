from flask import Blueprint

from views.ekart import EkartView, EkartIDView, CartItemsView, CartItemsIDView, WishListView, WishListIDView, SizesView, CategoryView

ekart = Blueprint("ekart", __name__)

ekart.add_url_rule("/", view_func=EkartView.as_view("ekart-list"), methods=["GET", "POST"])
ekart.add_url_rule("/<int:id>", view_func=EkartIDView.as_view("ekart-detail"),
                   methods=["GET", "PUT", "PATCH", "DELETE"])

ekart.add_url_rule("/cart", view_func=CartItemsView.as_view("cart-list"), methods=["GET", "POST"])
ekart.add_url_rule("/cart/<int:id>", view_func=CartItemsIDView.as_view("cart-detail"),
                   methods=["GET", "PUT", "PATCH", "DELETE"])

ekart.add_url_rule("/wish_list", view_func=WishListView.as_view("wish-list"), methods=["GET", "POST"])
ekart.add_url_rule("/wish_list/<int:id>", view_func=WishListIDView.as_view("wish-detail"),
                   methods=["GET", "DELETE"])

ekart.add_url_rule("/size_list", view_func=SizesView.as_view("size-list"), methods=["GET", "POST"])

ekart.add_url_rule("/categories", view_func=CategoryView.as_view("category-list"), methods=["GET", "POST"])
