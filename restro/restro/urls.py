
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from food.views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register(r"category", CategoryViewSet)
router.register(r"recipe", RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOtp.as_view()),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
