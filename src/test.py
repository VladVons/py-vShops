# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://www.youtube.com/watch?v=bu5wXjz2KvU
# https://console.developers.google.com

import re
import gspread


def Test_05():
    #Auth = '~/.config/gspread/service_account.json'
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sh = gc.open_by_url(Url)
    wsl = sh.worksheets()
    ws = sh.worksheet('MONITORS')
    print(ws.row_count, ws.col_count)
    Values = ws.get_all_values()
    

    pass


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def render1(template, data):
    pattern = r"\{\{\s*(\w+)\s*\}\}"
    result = re.sub(pattern, lambda match: str(data.get(match.group(1), "")), template)
    return result


def render(template, data):
    pattern = r"\{\{\s*(\w+)\s*\}\}"
    result = re.sub(pattern, lambda match: str(data.get(match.group(1), "")), template)
    if re.search(pattern, result):
        result = render(result, data)
    return result


def render_template(template, context):
    """
    Рекурсивна функція, що рендерить шаблон з використанням контексту.

    Args:
        template (str): Рядок з шаблоном.
        context (dict): Словник з контекстом, який буде використовуватись для підстановки змінних в шаблоні.

    Returns:
        str: Рядок з відображенням шаблону.
    """
    rendered_template = ""

    i = 0
    while i < len(template):
        # Пошук початку тегу "{{"
        if template[i:i + 2] == "{{":
            end_index = template.find("}}", i + 2)
            if end_index == -1:
                raise ValueError("Помилка: Неправильно відкритий тег '{{' у шаблоні")
            variable_name = template[i + 2:end_index].strip()
            rendered_template += str(context.get(variable_name, ""))
            i = end_index + 2

        # Пошук початку тегу "{%"
        elif template[i:i + 2] == "{%":
            end_index = template.find("%}", i + 2)
            if end_index == -1:
                raise ValueError("Помилка: Неправильно відкритий тег '{%' у шаблоні")
            statement = template[i + 2:end_index].strip()
            if statement.startswith("if"):
                # Обробка тегу {% if %}
                _, condition = statement.split("if")
                condition = condition.strip()
                if condition in context and context[condition]:
                    if_body = ""
                    j = end_index + 2
                    while j < len(template):
                        if template[j:j + 2] == "{%":
                            _, end_statement = template[j:].split("%}")
                            if end_statement.strip() == "endif":
                                rendered_template += render_template(if_body, context)
                                i = j + len(end_statement) + 2
                                break
                        if_body += template[j]
                        j += 1
                    else:
                        raise ValueError("Помилка: Незакритий тег '{%' у шаблоні")
                else:
                    i = end_index + 2

            elif statement.startswith("for"):
                # Обробка тегу {% for %}
                _, for_expr = statement.split("for")
                for_expr = for_expr.strip()
                variable_name, iterable_name = for_expr.split("in")
                variable_name = variable_name.strip()
                iterable_name = iterable_name.strip()
                iterable = context.get(iterable_name, [])
                for item in iterable:
                    inner_context = {**context, variable_name: item}
                    for_body = ""
                    j = end_index + 2
                    while j < len(template):
                        if template[j:j + 2] == "{%":
                            _, end_statement = template[j:].split("%}")
                            if end_statement.strip() == "endfor":
                                for_body_result = render_template(for_body, inner_context)
                                rendered_template += for_body_result


# Приклад використання
#template = "Hello, {{ name }}! You are {{ age }} years old. {{message}}"
#data = {"name": "John", "age": 30, "message": "{{ nested_message }}"}
#nested_data = {"nested_message": "Have a nice day!"}
#data.update(nested_data)
#print(render(template, data))


# Приклад використання
#template = "Hello, {{ name }}! You are {{ age }} years old."
#data = {"name": "John", "age": 30}
#print(render(template, data))


#Test_05()
#q1 = quick_sort([1,4,7,2,4,0,6,3,1])
#print(q1)


template = f'''
Hello, {{ name }}! You are {{ age }} years old
{% for %}
'''
data = {"name": "John", "age": 30}
print(render_template(template, data))
