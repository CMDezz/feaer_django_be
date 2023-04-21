from django.urls import path
from feaer_backend.apis.Product import Product_apis

urlpatterns = [
    # thêm xóa sửa 
    path('',Product_apis.getAll),
    path('createNewProduct',Product_apis.create),
    path('deleteProduct',Product_apis.deleteOne),
    path('editProduct',Product_apis.edit),
    # get thông tin sản phẩm theo id
    path('getProductById/<str:id>/',Product_apis.getProductById),
    # get danh sách những sản phẩm mới nhất
    path('getNewestProducts',Product_apis.getLatestProducts),
]