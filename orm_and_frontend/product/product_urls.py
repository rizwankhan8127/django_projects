from django.urls import path
from product import views

urlpatterns = [
    path('index/', views.index),
    path('filter/<category_value>', views.filter_by_category),
    path('sort/<sort_value>', views.sort_by_price),
    path('rating/<rating_value>', views.filter_by_rating),
    path('price', views.filter_by_price_range),
    path('product_details/<pid>',views.product_details),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart/',views.view_cart),
    path('remove_item/<cartid>',views.remove_item),
    path('update_quantity/<flag>/<cartid>',views.update_quantity),
    path('place_order',views.place_order)

]