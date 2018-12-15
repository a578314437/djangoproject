from django.urls import path
from .views import interFaceList,interFaceDetail,interFaceType
urlpatterns = [
    path('interFaceList/', interFaceList,name='interFaceList'),
    path('interFaceDetail/<int:interFace_pk>', interFaceDetail,name='interFaceDetail'),
    path('interFaceType/<int:interFace_type_pk>',interFaceType,name='interFaceType'),
]