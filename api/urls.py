from django.urls import path
from rest_framework.routers import DefaultRouter


from api.views import BookReviewAPIView, BookListAPIView, BookReviewListAPIView

app_name = 'api'



urlpatterns = [
    path('books/list/', BookListAPIView.as_view(), name='book-list'),
    path('reviews/<int:id>/', BookReviewAPIView.as_view(), name='review-detail'),
    path('reviews/', BookReviewListAPIView.as_view(), name='review-list'),
]

