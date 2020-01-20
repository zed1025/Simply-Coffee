from django.urls import path

from .views import order_details_view
from . import views


urlpatterns = [
    path('new/', views.new_user_view),
    path('new/add_new/', views.new_user_submit_view),
    path('existing_check/', views.existing_user_check_view),
    path('existing_check/is_existing/', views.is_existing),
    path('existing_check/is_existing/add_new/', views.new_user_submit_view),
    path('existing_check/is_existing/order_summary/', views.order_summary_view),
    path('new/add_new/order_summary/', views.order_summary_view),
]
