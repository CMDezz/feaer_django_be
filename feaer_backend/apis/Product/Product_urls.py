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
    # get danh sách theo thể loại
    path('getProductsByCategory/<str:name>/',Product_apis.getProductsByCategory),
    path('getProductsByCategoryId/<str:id>/',Product_apis.getProductsByCategoryId),

    # get danh sách theo tag
    path('getProductsByTag/<str:name>/',Product_apis.getProductsByTag),
    path('getProductsByTagId/<str:id>/',Product_apis.getProductsByTagId),

    #tìm kiếm sản phẩm theo tên
    path('getProductsByName/<str:name>/',Product_apis.getProductsByName),

    #get danh sách sản phẩm bán chạy
    path('getTopSellerProducts',Product_apis.getTopSellerProducts),

    #get danh sách sản phẩm có discount (name)
    path('getProductsByDiscount/<str:name>/',Product_apis.getProductsByDiscount),
    
    #get danh sách sản phẩm theo bộ sưu tập - collection (tên)
    path('getProductsByCollection/<str:name>/',Product_apis.getProductsByCollection),
    
    #get danh sách sản phẩm theo giới tính (tên)
    path('getProductsBySex/<str:name>/',Product_apis.getProductsByCollection),
    
]