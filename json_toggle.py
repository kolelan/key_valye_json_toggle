import json
import sys

# Конфигурационные переменные
NAME_KEY = "name"
DESC_KEY = "desc"

def detect_format(data):
    """Определяет формат входных данных"""
    if not data:
        return None
    first_item = data[0]
    if isinstance(first_item, dict) and NAME_KEY in first_item and DESC_KEY in first_item:
        return "format1"
    elif isinstance(first_item, dict) and len(first_item) == 1:
        return "format2"
    return None

def convert_format1_to_format2(data):
    """Преобразует из формата 1 в формат 2"""
    return [{item[NAME_KEY]: item[DESC_KEY]} for item in data]

def convert_format2_to_format1(data):
    """Преобразует из формата 2 в формат 1"""
    return [{NAME_KEY: key, DESC_KEY: value} for item in data for key, value in item.items()]

def process_json_file(input_file, output_file):
    """Обрабатывает JSON файл с сохранением компактного формата"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        detected_format = detect_format(data)

        if detected_format == "format1":
            converted_data = convert_format1_to_format2(data)
        elif detected_format == "format2":
            converted_data = convert_format2_to_format1(data)
        else:
            print("Неизвестный формат JSON файла")
            return False

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("[\n")  # Начало массива

            # Записываем каждый объект в компактном виде на отдельной строке
            for i, item in enumerate(converted_data):
                json.dump(item, f, ensure_ascii=False)
                if i < len(converted_data) - 1:
                    f.write(",\n")  # Запятая между элементами
                else:
                    f.write("\n")  # Последний элемент без запятой

            f.write("]")  # Конец массива

        print(f"Файл успешно преобразован и сохранен как {output_file}")
        return True

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python json_toggle.py <input_file.json> <output_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_json_file(input_file, output_file)