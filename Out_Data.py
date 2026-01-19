import json
from tabulate import tabulate

with open('boss_sieges_scores.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Создаем список для таблицы
table_data = []

# Проходим по всем членам клана
for member in data.get('members_info', []):
    name = member.get('name', 'Без имени')

    # Получаем значения из current scores
    current_scores = member.get('scores', {}).get('current', {})
    rating = current_scores.get('rating', '—')
    boss_siege = current_scores.get('boss_siege', '—')

    # Если значения None, заменяем на прочерк
    if rating is None:
        rating = '—'
    if boss_siege is None:
        boss_siege = '—'

    # Добавляем в таблицу
    table_data.append([name, rating, boss_siege])


# Сортируем по rating (сначала самые высокие, None/прочерки в конце)
def sort_key(row):
    rating = row[1]
    # Если rating — число, возвращаем его отрицательным (для сортировки по убыванию)
    if isinstance(rating, (int, float)):
        return -rating
    # Иначе возвращаем большое число, чтобы прочерки были в конце
    return float('inf')


table_data.sort(key=sort_key)

# Выводим таблицу
headers = ["Имя игрока", "Rating (current)", "Boss Siege (current)"]
print(tabulate(table_data, headers=headers, tablefmt="grid", numalign="right", stralign="left"))
