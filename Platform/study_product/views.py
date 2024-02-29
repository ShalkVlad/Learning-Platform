from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Lesson, Group


# Определяем представление API для получения доступных продуктов
@api_view(['GET'])
def available_products(request):
    # Получаем все продукты из базы данных
    products = Product.objects.all()
    data = []
    # Для каждого продукта собираем информацию о количестве уроков и добавляем в список данных
    for product in products:
        num_lessons = Lesson.objects.filter(product=product).count()
        data.append({
            'name': product.name,
            'start_date': product.start_date,
            'cost': product.cost,
            'num_lessons': num_lessons
        })
    # Возвращаем ответ с данными о продуктах
    return Response(data)


# Определяем представление API для получения уроков продукта по его идентификатору
@api_view(['GET'])
def product_lessons(request, product_id):
    # Получаем объект продукта по его идентификатору
    product = get_object_or_404(Product, pk=product_id)
    # Получаем текущего пользователя
    user = request.user
    # Проверяем, есть ли у пользователя доступ к урокам данного продукта
    groups = Group.objects.filter(product=product, students=user)
    if not groups:
        # Если доступа нет, возвращаем ошибку 403
        return Response({"detail": "У вас нет доступа к урокам по этому продукту."}, status=403)
    # Получаем все уроки данного продукта
    lessons = Lesson.objects.filter(product=product)
    data = []
    # Формируем данные о каждом уроке и добавляем в список данных
    for lesson in lessons:
        data.append({
            'name': lesson.name,
            'video_link': lesson.video_link
        })
    # Возвращаем ответ с данными о уроках продукта
    return Response(data)


# Определяем функцию для распределения пользователя по группам продукта
def distribute_user(user, product):
    # Проверяем, если дата начала продукта в будущем, то добавляем пользователя в группу с наименьшим числом учеников
    if product.start_date > datetime.now():
        groups = product.group_set.annotate(num_students=Count('students')).order_by('num_students')
        target_group = groups.first()
        target_group.students.add(user)
    # Если дата начала продукта уже прошла, то добавляем пользователя в группу с количеством учеников ниже среднего
    else:
        groups = product.group_set.annotate(num_students=Count('students')).order_by('-num_students')
        average_students = sum(group.num_students for group in groups) / len(groups)
        for group in groups:
            if group.num_students < average_students:
                group.students.add(user)
                break


@api_view(['GET'])
def product_statistics(request, product_id):
    # Получаем объект продукта по его идентификатору
    product = get_object_or_404(Product, pk=product_id)

    # 1. Количество учеников занимающихся на продукте
    num_students = Group.objects.filter(product=product).aggregate(total_students=Count('students'))[
                       'total_students'] or 0

    # 2. Процент заполненности групп
    max_users = product.max_users
    avg_students = Group.objects.filter(product=product).aggregate(avg_students=Count('students') / max_users)[
                       'avg_students'] or 0
    fill_percent = (avg_students / max_users) * 100 if max_users > 0 else 0

    # 3. Процент приобретения продукта
    total_users = User.objects.count()  # Общее количество пользователей на платформе
    access_count = product.group_set.count()  # Количество полученных доступов к продукту
    purchase_percent = (access_count / total_users) * 100 if total_users > 0 else 0

    # Формируем данные о статистике продукта
    data = {
        'num_students': num_students,
        'fill_percent': fill_percent,
        'purchase_percent': purchase_percent
    }

    # Возвращаем ответ с данными о статистике продукта
    return Response(data)


@api_view(['GET'])
def product_statistics_list(request):
    # Получаем все продукты из базы данных
    products = Product.objects.all()
    data = []

    # Для каждого продукта рассчитываем статистику и добавляем в список данных
    for product in products:
        # 1. Количество учеников занимающихся на продукте
        num_students = Group.objects.filter(product=product).aggregate(total_students=Count('students'))[
                           'total_students'] or 0

        # 2. Процент заполненности групп
        max_users = product.max_users
        avg_students = Group.objects.filter(product=product).aggregate(avg_students=Count('students') / max_users)[
                           'avg_students'] or 0
        fill_percent = (avg_students / max_users) * 100 if max_users > 0 else 0

        # 3. Процент приобретения продукта
        total_users = User.objects.count()
        access_count = product.group_set.count()
        purchase_percent = (access_count / total_users) * 100 if total_users > 0 else 0

        # Формируем данные о статистике продукта
        product_data = {
            'product_id': product.id,
            'product_name': product.name,
            'num_students': num_students,
            'fill_percent': fill_percent,
            'purchase_percent': purchase_percent
        }

        data.append(product_data)

    # Возвращаем ответ с данными о статистике продуктов
    return Response(data)
