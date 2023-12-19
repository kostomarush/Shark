import csv

# Имя CSV файла
filename = 'allitems.csv'
rows_to_save = [0, 2]
selected_rows = []
# Открываем CSV файл для чтения и записи
with open(filename, 'r', newline='') as file:
    # Читаем содержимое CSV файла
    reader = csv.reader(file)
    rows = list(reader)

# Заменяем первую запятую в каждой строке на точку с запятой
for row in rows:
    #row[0] = row[0].replace(f'{row[0]}', f'{row[0]};')
    # Если текущий индекс строки содержится в списке rows_to_save, сохраняем строку
    if row[2]!='':
        if row[0]!='Name' and row[0]!='Description':
            selected_rows.append([row[0], row[2]])
    else:
        pass
# Создаем новый CSV файл и записываем в него выбранные строки
new_filename = 'output.csv'
with open(new_filename, 'w', newline='') as file:
    # Создаем объект writer для записи в CSV файл
    writer = csv.writer(file, delimiter=';')
    # Записываем выбранные строки в CSV файл
    writer.writerows(selected_rows)

print('Сохранение выполнено успешно.')
