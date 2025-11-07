from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author, BookAuthor, BookReview
from users.models import CustomUser


class BooksTests(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        Book.objects.create(title='Book 1', description='Some description', isbn='12345' )
        Book.objects.create(title='Book 2', description='Some description 2', isbn='123456')


        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)


    def test_books_detail(self):
        Book.objects.create(title='Book 1', description='Some description', isbn='12345' )
        book = Book.objects.get(title='Book 1')
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_book_author(self):
        Book.objects.create(title='Book 1', description='Some description', isbn='12345' )
        book = Book.objects.get(title='Book 1')
        Author.objects.create(first_name='Azamatjon', last_name='Abdulazizov')
        author = Author.objects.get(first_name='Azamatjon')
        BookAuthor.objects.create(author=author, book=book)

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)






    def test_search_books(self):
        book1 = Book.objects.create(title='sports', description='Some description', isbn='12345' )
        book2 = Book.objects.create(title='Halloween', description='Some description 2', isbn='123456')
        response = self.client.get(reverse('books:list') + "?q=sports")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)

        response = self.client.get(reverse('books:list') + "?q=Halloween")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)



class BookReviewTests(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345' )
        user = CustomUser.objects.create_user(username='user', password='password')
        user.save()
        self.client.login(username='user', password='password')

        self.client.post(reverse('books:reviews', kwargs={'id': book.id}), {
            "stars_given": 5,
            "comment": "Some comment",
        })
        book_review = book.bookreview_set.all()
        assert len(book_review) == 1
        self.assertEqual(book_review[0].comment, "Some comment")
        self.assertEqual(book_review[0].stars_given, 5)


    def test_edit_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        user = CustomUser.objects.create_user(username='user', password='password')
        user.save()
        self.client.login(username='user', password='password')

        book_review = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Some comment")
        book_review.save()

        response = self.client.post(reverse('books:edit-review', kwargs={'book_id': book.id, "review_id": book_review.id}),
                                    {
            "stars_given": 3,
            "comment": "Some comment!!!",
        })

        self.assertEqual(response.status_code, 302)
        book_review.refresh_from_db()
        self.assertEqual(book_review.stars_given, 3)
        self.assertEqual(book_review.comment, "Some comment!!!")


    def test_delete_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        user = CustomUser.objects.create_user(username='user', password='password')
        user.save()
        self.client.login(username='user', password='password')

        book_review = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Some comment")
        book_review.save()

        response = self.client.post(reverse('books:delete-review', kwargs={'book_id': book.id, 'review_id': book_review.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:detail', kwargs={'id': book.id}))

        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())














