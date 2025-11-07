from django.core.paginator import Paginator
from rest_framework import status, generics, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book, BookReview
from api.serializers import BookReviewSerializer, BookSerializer


# class BookReviewsViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = BookReview.objects.all()
#     serializer_class = BookReviewSerializer
#     lookup_field = 'id'


class BookReviewAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    lookup_field = 'id'

    # def get(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(book_review)
    #
    #     return Response(serializer.data)
    #
    # def delete(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     book_review.delete()
    #     data = {
    #         'status': 'success',
    #         'message': 'Book Review Deleted',
    #     }
    #     return Response(status=status.HTTP_200_OK, data=data)
    #
    # def put(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(book_review, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def patch(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(book_review, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookReviewListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    pagination_class = PageNumberPagination
    paginate_by = 3

    # def post(self, request):
    #     serializer = BookReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class BookListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all().order_by('-id')
    paginate_by = 2
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

