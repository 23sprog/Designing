from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'preview/(?P<slug>[-\w]+)/', ProductDetailPreview.as_view(), name="preview_product"),
    re_path(r'view/(?P<slug>[-\w]+)/', ProductDetailView.as_view(), name="view_product"),
    path('comment/', ProductCommentView.as_view(), name="comment_product"),
    path('list/', ProductListView.as_view(), name="list_product"),
    path('list/page/<int:page>/', ProductListView.as_view(), name="list_product"),
    path('update/<int:id>/', ProductUpdateView.as_view(), name="update_product"),
    path('delete/<int:id>/', ProductDeleteView.as_view(), name="delete_product"),
    path('product_cart/delete/<int:id>/', ProductDeleteCartView.as_view(), name="delete_product_cart"),
    path('product_cart/list/', ProductCartView.as_view(), name="list_product_cart"),
    path('product_cart/final_section/', ProductCartFinalSectionView.as_view(), name="final_section_product_cart"),
    path('product_cart/add/', ProductAddToCartView.as_view(), name="add_product_cart"),
    path('create/', ProductCreateView.as_view(), name="create_product"),
    path('shop/', ShopPanelView.as_view(), name="view_shop"),
    path('shop/page/<int:page>/', ShopPanelView.as_view(), name="view_shop"),
    path('shop/create/admin/', AdminShopCreateView.as_view(), name="create_shop_admin"),
    path('shop/create/near_seller/', NearSellerShopCreateView.as_view(), name="create_shop_near_seller"),
    path('shop/update/admin/<int:id>/', AdminShopUpdateView.as_view(), name="admin_update_shop"),
    path('shop/update/seller/<int:id>/', SellerShopUpdateView.as_view(), name="seller_update_shop"),
    path('shop/delete/<int:id>/', ShopDeleteView.as_view(), name="delete_shop"),
    path('shop/detail/<int:id>/', ShopDetailView.as_view(), name="detail_shop"),
]
app_name = "products"


