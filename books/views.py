from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from books.forms import BookReviewForm
from books.models import Book, BookReview


class BooksView(ListView):
    template_name = "books/list.html"
    context_object_name = "books"
    queryset = Book.objects.all()
    paginate_by = 4
    search_fields = ["title", "author"]
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            queryset = Book.objects.filter(
                title__icontains=query
            )
            return queryset
        return Book.objects.all()








# class BooksView(View):
#     def get(self, request):
#         books = Book.objects.all().order_by('id')
#         paginator = Paginator(books, 2)
#         page_obj = paginator.get_page(request.GET.get('page'))
#
#         return render(request, 'books/list.html', {'page_obj': page_obj})

# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "id"
#     model = Book

class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()


        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})



class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given = review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment'],
            )
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})




class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, 'books/delete_review.html', {'book': book, 'review': review})



class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, 'Review deleted successfully')
        return redirect(reverse('books:detail', kwargs={'id': book.id}))





