from http.client import responses
from django.test import TestCase
from django.urls import reverse

from books.models import BookReview, Book
from users.models import CustomUser


class HomePageTest(TestCase):
    def test_paginated_test(self):
        book1 = Book.objects.create(title='Book 1', description='Some description', isbn='12345')
        user = CustomUser.objects.create_user(username='user', password='password')
        user.save()
        self.client.login(username='user', password='password')
        review1 = BookReview.objects.create(book=book1, user=user, stars_given=3, comment='Some comment')
        review2 = BookReview.objects.create(book=book1, user=user, stars_given=4, comment='Some comment 2')
        review3 = BookReview.objects.create(book=book1, user=user, stars_given=5, comment='Some comment 3')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.stars_given)
        self.assertContains(response, review2.stars_given)

