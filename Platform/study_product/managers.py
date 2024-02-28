from datetime import datetime
from django.db.models import Count


def distribute_user_to_group(user, product):
    # Проверяем, начался ли продукт
    if product.start_date > datetime.now():
        # Получаем все группы для данного продукта, сортируем их по количеству участников
        groups = product.group_set.annotate(num_students=Count('students')).order_by('num_students')

        # Выбираем группу с наименьшим количеством участников
        target_group = groups.first()

        # Добавляем пользователя в эту группу
        target_group.students.add(user)
    else:
        # Пересобираем группы, чтобы в них было примерно одинаковое количество участников
        groups = product.group_set.annotate(num_students=Count('students')).order_by('-num_students')

        # Рассчитываем среднее количество участников в группе
        average_students = sum(group.num_students for group in groups) / len(groups)

        # Находим первую группу, в которую можно добавить пользователя без превышения среднего количества участников
        for group in groups:
            if group.num_students < average_students:
                # Добавляем пользователя в эту группу
                group.students.add(user)
                break
