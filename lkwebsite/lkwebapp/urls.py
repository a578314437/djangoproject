from django.urls import path
from .views import interFaceList,interFaceDetail,interFaceTypeList
urlpatterns = [
    path('interFaceList/', interFaceList,name='interFaceList'),
    path('interFaceDetail/<int:interFace_pk>', interFaceDetail,name='interFaceDetail'),
    path('interFaceTypeList/<int:interFace_type_pk>',interFaceTypeList,name='interFaceTypeList'),
]