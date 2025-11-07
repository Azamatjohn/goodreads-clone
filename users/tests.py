from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse



class RegistrationTests(TestCase):
    def test_user_account_is_created(self):
        self.client.post(reverse('users:register'), {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': '321123',
            'first_name': 'test',
            'last_name': 'test'
        })

        user = CustomUser.objects.get(username='test')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'test')
        self.assertNotEqual(user.password, '321123')
        self.assertTrue(user.check_password('321123'))


    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            {'first_name': 'test', 'email': 'test@gmail.com',})


        user_count = CustomUser.objects.count()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(user_count, 0)
        # self.assertFormError(response, 'form', 'username', 'This field is required.')


class LoginTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test',
            email='test@gmail.com',
        )
        self.user.set_password('321123')
        self.user.save()

    def test_successful_login(self):

        self.client.post(reverse('users:login'), {'username': 'test', 'password': '321123'})

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):

        self.client.post(reverse('users:login'), {'username': 'wrong_username', 'password': '321123'})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(reverse('users:login'), {'username': 'test', 'password': 'wrong_password'})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):

        self.client.login(username='test', password='321123')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)



class ProfileTests(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.url, reverse('users:login') + "?next=/users/profile/")
        self.assertEqual(response.status_code, 302)



    def test_profile_details(self):
        user = CustomUser.objects.create_user(
            username='test',
            email='test@gmail.com',
            first_name='test1111',
            last_name='test2222'
        )
        user.set_password('12345')
        user.save()


        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)


    def test_update_profile(self):
        user = CustomUser.objects.create_user(
            username='test',
            email='test@gmail.com',
            first_name='test1111',
            last_name='test2222'
        )
        user.set_password('12345')
        user.save()
        self.client.login(username='test', password='12345')
        response = self.client.post(reverse('users:profile-update'), {
            'username': 'test',
            'password': '12345',
            'first_name': 'test12',
            'last_name': 'test2222',
            'email': 'test123212@gmail.com',
        })
        # user = User.objects.get(pk=user.pk)
        user.refresh_from_db()


        self.assertEqual(user.first_name, 'test12')
        self.assertEqual(user.email, 'test123212@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))








