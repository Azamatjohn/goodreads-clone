from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test',
            email='test@gmail.com',
        )
        self.user.set_password('321123')
        self.user.save()
        self.client.login(username='test', password='321123')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345' )
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='Some comment')

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], 'Some comment')

        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book 1')
        self.assertEqual(response.data['book']['description'], 'Some description')

        self.assertEqual(response.data['user']['username'], 'test')

    def test_delete_book_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='Some comment')

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': br.id}),)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_book_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='Some comment')
        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), {
            'stars_given': 5,
        })
        br.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stars_given'], 5)

    def test_put_book_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='Some comment')
        response = self.client.put(reverse('api:review-detail', kwargs={'id': br.id}), {
            'stars_given': 5,
            'comment': 'nice book',
            'user_id': self.user.id,
            'book_id': book.id
        })
        br.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'nice book')

    def test_create_book_review(self):
        book = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        data = {
            'stars_given': 2,
            'comment': 'bad book',
            'user_id': self.user.id,
            'book_id': book.id
        }
        response = self.client.post(reverse('api:review-list'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stars_given'], 2)
        self.assertEqual(response.data['comment'], 'bad book')











    def test_book_list(self):
        book_1 = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        book_2 = Book.objects.create(title='Book 2', description='Some description 2', isbn='123456')
        book_3 = Book.objects.create(title='Book 3', description='Some description 3', isbn='1234567')

        response = self.client.get(reverse('api:book-list'))


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)







