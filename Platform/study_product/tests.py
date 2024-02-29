import os
import unittest

import django

# Установите переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Platform.settings')
django.setup()
# Модули, что использую при тестах
from django.test import TestCase
from django.contrib.auth.models import User
from study_product.models import Product, Lesson, Group
from study_product.views import distribute_user
from django.urls import reverse
from django.utils import timezone


class AvailableProductsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.product = Product.objects.create(name='Test Product', creator=self.user, start_date='2024-02-28 12:00:00',
                                              cost=10)

    def test_available_products(self):
        # Тест на доступность продуктов
        url = reverse('available_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)


class ProductLessonsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.product = Product.objects.create(name='Test Product', creator=self.user, start_date='2024-02-28 12:00:00',
                                              cost=10)
        self.lesson = Lesson.objects.create(name='Test Lesson', video_link='http://example.com', product=self.product)

    def test_product_lessons(self):
        # Тест на уроки продукта
        url = reverse('product_lessons', kwargs={'product_id': self.product.id})
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class DistributionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.product = Product.objects.create(name='Test Product', creator=self.user, start_date='2024-02-28 12:00:00',
                                              cost=10, min_users=1, max_users=10)
        self.group = Group.objects.create(name='Test Group', product=self.product)

    def test_distribution(self):
        # Тест на распределение
        naive_start_date = self.product.start_date.replace(tzinfo=None)
        naive_now = timezone.localtime(timezone.now()).replace(tzinfo=None)
        if naive_start_date > naive_now:
            distribute_user(self.user, self.product)
            self.assertIn(self.user, self.group.students.all())


class ProductStatisticsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.product = Product.objects.create(name='Test Product', creator=self.user, start_date='2024-02-28 12:00:00',
                                              cost=10, min_users=1, max_users=10)
        self.group = Group.objects.create(name='Test Group', product=self.product)
        # Добавляем пользователя в группу
        self.group.students.add(self.user)

    def test_product_statistics(self):
        # Тест на проверку статистики продукта
        url = reverse('product_statistics', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['num_students'], 1)
        # Проверяем, что процент заполненности групп и процент приобретения продукта находятся в допустимых пределах
        self.assertTrue(0 <= data['fill_percent'] <= 100)
        self.assertTrue(0 <= data['purchase_percent'] <= 100)


class ProductStatisticsListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.product = Product.objects.create(name='Test Product', creator=self.user, start_date='2024-02-28 12:00:00',
                                              cost=10, min_users=1, max_users=10)
        self.group = Group.objects.create(name='Test Group', product=self.product)
        # Добавляем пользователя в группу
        self.group.students.add(self.user)

    def test_product_statistics_list(self):
        # Тест на проверку статистики продуктов
        url = reverse('product_statistics_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list) and len(data) > 0)
        for product_data in data:
            self.assertTrue('product_id' in product_data)
            self.assertTrue('product_name' in product_data)
            self.assertTrue('num_students' in product_data)
            self.assertTrue('fill_percent' in product_data)
            self.assertTrue('purchase_percent' in product_data)
            # Проверяем, что процент заполненности групп и процент приобретения продукта находятся в допустимых пределах
            self.assertTrue(0 <= product_data['fill_percent'] <= 100)
            self.assertTrue(0 <= product_data['purchase_percent'] <= 100)


if __name__ == '__main__':
    unittest.main()
