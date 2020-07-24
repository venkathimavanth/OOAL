from django.urls import path,include,re_path
from . import views

app_name = "business"


urlpatterns = [
    path('limited_offer_coupons/',views.coupon_upload,name='coupon_upload'),
    path('collaberate/',views.collaberate_home,name='collaberate'),
    path('perminent_coupons/',views.perminent_coupons,name='add_coupon'),
    # path('video_upload/',views.video_check),
    path('video_view/',views.video_view),
    # path('fun/',views.Fun_View.as_view(),name='fun'),
    path('fun/',views.fun,name='fun'),
    path('stats/',views.stats,name='stats'),

]
