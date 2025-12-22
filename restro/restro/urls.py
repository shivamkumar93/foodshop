
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from food.views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from food.admin_views import *

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

router.register(r"category", CategoryViewSet, basename='category')
router.register(r"recipe", RecipeViewSet, basename='recipe')
router.register(r"forgotPassword", ForgotPasswordView, basename='forgot')
router.register(r"authlogin",LoginAPIView, basename='login')
router.register(r"order", OrderViewSet, basename='order')
router.register(r"address", AddressView, basename='address')
router.register(r"recipevarint", RecipeVariantView, basename='recipevarint')
router.register(r"recipetype", RecipeTypeView, basename='recipetype')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger/',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    #path('login/', obtain_auth_token),
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOtp.as_view()),
    path('paymentVerify/', VerifyPaymentApiview.as_view()),
    
    path('payment/', verify),

    # django views urls here
    path("categoryform/", category, name="categoryform"),
    path("recipeform/", recipe, name="recipeform"),
    path("recipetypeform/", recipetype, name="recipetypeform"),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
