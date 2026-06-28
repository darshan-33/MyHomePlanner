"""
URL configuration for estimation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('reg',views.reg,name='reg'),
    path('contractor_dashboard',views.contractor_dashboard,name='contractor_dashboard'),
    path('labour_dashboard',views.labour_dashboard,name='labour_dashboard'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('add_contractor',views.add_contractor,name='add_contractor'),
    path('contractor_view',views.contractor_view,name='contractor_view'),
    path('add_labour',views.add_labour,name='add_labour'),
    path('labour_view',views.labour_view,name='labour_view'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('estimation/<str:house>',views.estimation,name='estimation'),
    path('sale_house',views.sale_house,name='sale_house'),
    path('sale_house_view',views.sale_house_view,name='sale_house_view'),
    path('sale_house_view_u', views.sale_house_view_u, name='sale_house_view_u'),
    path('house_book_request/<int:pk>',views.house_book_request,name='house_book_request'),
    path('book_request_status',views.book_request_status,name='book_request_status'),

    path('update_sale_status/<int:pk>',views.update_sale_status,name='update_sale_status'),

    path('service_status_view',views.service_status_view,name='service_status_view'),
    path('market_price',views.market_price,name='market_price'),
    path('market_price_view_u',views.market_price_view_u,name='market_price_view_u'),
    path('market_price_view',views.market_price_view,name='market_price_view'),

    path('service_request/<int:pk>',views.service_request,name='service_request'),
    path('view_contractors',views.view_contractors,name='view_contractors'),
    path('sale_house_del/<int:pk>',views.sale_house_del,name='sale_house_del'),
    path('blueprint_del/<int:pk>',views.blueprint_del,name='blueprint_del'),
    path('upload_blue_print',views.upload_blue_print,name='upload_blue_print'),
    path('upload_blue_print_view',views.upload_blue_print_view,name='upload_blue_print_view'),
    #path('vr-view/', views.vr_view, name='vr_view'),
    #path('vr-view/<str:bhk_type>/', views.vr_view, name='vr_view'),
    path('vr-view/<str:bhk_type>/', views.vr_view, name='vr_view'),
    path('update_service_status/<int:pk>',views.update_service_status,name='update_service_status'),

    path('contra_req_view',views.contra_req_view,name='contra_req_view'),
    path('book_request_view',views.book_request_view,name='book_request_view'),
    path('labours_view',views.labours_view,name='labours_view'),
    path('contractor_del/<int:pk>',views.contractor_del,name='contractor_del'),
    path('labour_del/<int:pk>',views.labour_del,name='labour_del'),
    path('market_del/<int:pk>', views.market_del, name='market_del'),
    path('logout/', views.logout_view, name='logout'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
