from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes),
    path('<int:pk>', views.getRoute),
    path('rooms', views.getRooms),
    path('rooms/<int:pk>', views.getRoom),
]