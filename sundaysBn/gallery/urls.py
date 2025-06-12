from django.urls import path
from .views import OwnerRegisterView, OwnerLoginView, ArtPieceListCreateView, ArtPieceDetailView

urlpatterns = [
    path('register/', OwnerRegisterView.as_view(), name='owner-register'),
    path('login/', OwnerLoginView.as_view(), name='owner-login'),
    path('art-pieces/', ArtPieceListCreateView.as_view(), name='art-piece-list-create'),
    path('art-pieces/<int:pk>/', ArtPieceDetailView.as_view(), name='art-piece-detail'),
]