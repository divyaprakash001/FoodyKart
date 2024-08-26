from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path("",AccountViews.vendorDashboard,name='vendor'),
    path('profile/',views.vprofile, name="vprofile"),

    path('menu-builder',views.menu_builder, name="menu_builder"),
    path("menu-builder/category/<int:pk>/",views.fooditems_by_category,name="fooditems_by_category"),

    # category crud
    path('menu-builder/category/add/',views.add_category,name="add_category"),
    path('menu-builder/category/edit/<int:id>/',views.edit_category,name="edit_category"),
    path('menu-builder/category/delete/<int:id>/',views.delete_category,name="delete_category"),

    # food crud
    path('menu-builder/food/add/',views.add_food,name="add_food"),
    path('menu-builder/food/edit/<int:id>/',views.edit_food,name="edit_food"),
    path('menu-builder/food/delete/<int:id>/',views.delete_food,name="delete_food"),
]
