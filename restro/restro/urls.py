
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from food.views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"singup", SingupViewSet, basename='singup')
router.register(r"category", CategoryViewSet)
router.register(r"recipe", RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', obtain_auth_token)
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
