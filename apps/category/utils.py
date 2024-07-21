from .models import Category


def update_category_priority(category, new_priority):
    current_priority = int(category.priority)
    new_priority = int(new_priority)

    if current_priority > new_priority:
        priority_range = range(new_priority, current_priority)
        obj_list = Category.objects.filter(priority__in=priority_range)
        for obj in obj_list:
            obj.priority += 1
            obj.save()

    elif current_priority < new_priority:
        priority_range = range(current_priority + 1, new_priority + 1)
        obj_list = Category.objects.filter(priority__in=priority_range)
        for obj in obj_list:
            obj.priority -= 1
            obj.save()


def reorder_catagories(restaurant):
    categories = Category.objects.filter(restaurant=restaurant).order_by("priority")
    for index, category in enumerate(categories, start=1):
        category.priority = index
        category.save()
