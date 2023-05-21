from django.urls import path,include
urlpatterns = [
    path('sex/',include('feaer_backend.apis.Sex.Sex_urls')),
    path('tag/',include('feaer_backend.apis.Tag.Tag_urls')),
    path('discount/',include('feaer_backend.apis.Discount.Discount_urls')),
    path('collection/',include('feaer_backend.apis.Collection.Collection_urls')),
    path('contact/',include('feaer_backend.apis.Contact.Contact_urls')),
    path('category/',include('feaer_backend.apis.Category.Category_urls')),
    path('product/',include('feaer_backend.apis.Product.Product_urls')),
    path('order/',include('feaer_backend.apis.Order.Order_urls')),
    path('user/',include('feaer_backend.apis.User.User_urls')),
]