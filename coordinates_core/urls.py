from django.contrib import admin
from django.urls import path
from coordinates import views   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('directions/', views.directions_view, name='directions_view'),
]

