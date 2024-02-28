from datetime import datetime

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
def distribute_user_to_group(user, product):
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
