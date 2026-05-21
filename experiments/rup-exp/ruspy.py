"""
╔══════════════════════════════════════════════════════════════╗
║                    🇷🇺 RusPy v1.0 🇷🇺                        ║
║          Транслятор русского синтаксиса в Python             ║
║                                                              ║
║  Пишешь код на русском — он выполняется на Python.           ║
║  Создано как эксперимент Тьютора (Фаза 0, Week 3).          ║
╚══════════════════════════════════════════════════════════════╝

Использование:
    python ruspy.py программа.рус
    python ruspy.py --показать программа.рус   (показать сгенерированный Python-код)
    python ruspy.py --помощь                    (справка)
"""

import sys
import re
import os
import io

# Принудительно переключаем консоль Windows на UTF-8
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ═══════════════════════════════════════════════════════════
# 1. СЛОВАРЬ КЛЮЧЕВЫХ СЛОВ (Русский -> Python)
# ═══════════════════════════════════════════════════════════

KEYWORDS = {
    # --- Управляющие конструкции ---
    "Если":         "if",
    "ИначеЕсли":    "elif",
    "Иначе":        "else",
    "Пока":         "while",
    "Для":          "for",
    "В":            "in",
    "Диапазон":     "range",
    "Прервать":     "break",
    "Продолжить":   "continue",
    "Пропустить":   "pass",

    # --- Функции и классы ---
    "Функция":      "def",
    "Процедура":    "def",
    "Класс":        "class",
    "Вернуть":      "return",
    "Лямбда":       "lambda",

    # --- Логические операторы ---
    "И":            "and",
    "Или":          "or",
    "Не":           "not",
    "Истина":       "True",
    "Ложь":         "False",
    "Ничего":       "None",
    "Пусто":        "None",

    # --- Контекст и исключения ---
    "Попытка":      "try",
    "Исключение":   "except",
    "Наконец":      "finally",
    "Вызвать":      "raise",
    "Утверждать":   "assert",
    "С":            "with",
    "Как":          "as",

    # --- Импорт ---
    "Импорт":       "import",
    "Из":           "from",

    # --- Прочее ---
    "Глобальная":   "global",
    "Удалить":      "del",
    "Выход":        "yield",
}

# ═══════════════════════════════════════════════════════════
# 2. СЛОВАРЬ ВСТРОЕННЫХ ФУНКЦИЙ (Русский -> Python)
# ═══════════════════════════════════════════════════════════

BUILTINS = {
    # --- Ввод/Вывод ---
    "Сообщить":         "print",
    "Ввод":             "input",
    "Открыть":          "open",

    # --- Преобразование типов ---
    "Целое":            "int",
    "Дробное":          "float",
    "Строка":           "str",
    "Булево":           "bool",
    "Список":           "list",
    "Кортеж":           "tuple",
    "Словарь":          "dict",
    "Множество":        "set",
    "Байты":            "bytes",

    # --- Работа с коллекциями ---
    "Длина":            "len",
    "Диапазон":         "range",
    "Перечислить":      "enumerate",
    "Архивировать":     "zip",
    "Карта":            "map",
    "Фильтр":           "filter",
    "Сортировать":      "sorted",
    "Обратить":         "reversed",
    "Все":              "all",
    "Любой":            "any",
    "Сумма":            "sum",
    "Мин":              "min",
    "Макс":             "max",
    "Абс":              "abs",
    "Округлить":        "round",

    # --- Работа с объектами ---
    "Тип":              "type",
    "ЭтоЭкземпляр":    "isinstance",
    "ЭтоПодкласс":     "issubclass",
    "ЕстьАтрибут":     "hasattr",
    "ПолучитьАтрибут":  "getattr",
    "УстАтрибут":      "setattr",
    "Идентификатор":    "id",
    "Хеш":              "hash",
    "Вызываемый":       "callable",
    "Представление":    "repr",

    # --- Прочее ---
    "Выполнить":        "exec",
    "Вычислить":        "eval",
    "Формат":           "format",
    "Символ":           "chr",
    "КодСимвола":       "ord",
    "Двоичный":         "bin",
    "Восьмеричный":     "oct",
    "Шестнадцатеричный":"hex",
    "Степень":          "pow",
    "Делимод":          "divmod",
    "Срез":             "slice",
    "Супер":            "super",
    "Статический":      "staticmethod",
    "КлассМетод":       "classmethod",
    "Свойство":         "property",
}

# ═══════════════════════════════════════════════════════════
# 3. СЛОВАРЬ МЕТОДОВ (для строк, списков и словарей)
# ═══════════════════════════════════════════════════════════

METHODS = {
    # --- Методы строк ---
    ".верхний()":           ".upper()",
    ".нижний()":            ".lower()",
    ".заголовок()":         ".title()",
    ".полоса()":            ".strip()",
    ".лполоса()":           ".lstrip()",
    ".пполоса()":           ".rstrip()",
    ".начинается(":         ".startswith(",
    ".заканчивается(":      ".endswith(",
    ".найти(":              ".find(",
    ".заменить(":           ".replace(",
    ".разделить(":          ".split(",
    ".соединить(":          ".join(",
    ".считать(":            ".count(",
    ".центр(":              ".center(",
    ".форматировать(":      ".format(",
    ".являетсяЧислом()":   ".isdigit()",
    ".являетсяБуквой()":   ".isalpha()",
    ".являетсяПробелом()":  ".isspace()",

    # --- Методы списков ---
    ".добавить(":           ".append(",
    ".вставить(":           ".insert(",
    ".удалить(":            ".remove(",
    ".извлечь(":            ".pop(",
    ".извлечь()":           ".pop()",
    ".очистить()":          ".clear()",
    ".копировать()":        ".copy()",
    ".расширить(":          ".extend(",
    ".индекс(":             ".index(",
    ".сортировать()":       ".sort()",
    ".обратить()":          ".reverse()",

    # --- Методы словарей ---
    ".ключи()":             ".keys()",
    ".значения()":          ".values()",
    ".элементы()":          ".items()",
    ".получить(":           ".get(",
    ".обновить(":           ".update(",
    ".удалитьКлюч(":        ".pop(",

    # --- Методы файлов ---
    ".читать()":            ".read()",
    ".читатьСтроки()":      ".readlines()",
    ".читатьСтроку()":      ".readline()",
    ".писать(":             ".write(",
    ".закрыть()":           ".close()",
}

# ═══════════════════════════════════════════════════════════
# 4. МАГИЧЕСКИЕ МЕТОДЫ (Dunder methods)
# ═══════════════════════════════════════════════════════════

DUNDER = {
    "Функция __создать__":   "def __init__",
    "Функция __строка__":    "def __str__",
    "Функция __представление__": "def __repr__",
    "Функция __длина__":     "def __len__",
    "Функция __сложить__":   "def __add__",
    "Функция __равно__":     "def __eq__",
    "Функция __меньше__":    "def __lt__",
    "Функция __вход__":      "def __enter__",
    "Функция __выход__":     "def __exit__",
    "Процедура __создать__": "def __init__",
    "Процедура __строка__":  "def __str__",
}

# ═══════════════════════════════════════════════════════════
# 5. СЛОВАРЬ СТАНДАРТНЫХ МОДУЛЕЙ
# ═══════════════════════════════════════════════════════════

MODULES = {
    "математика":   "math",
    "случайный":    "random",
    "время":        "time",
    "система":      "sys",
    "ос":           "os",
    "json":         "json",
    "дата":         "datetime",
}

# Атрибуты модулей (часто используемые)
MODULE_ATTRS = {
    # math
    "математика.пи":            "math.pi",
    "математика.корень(":       "math.sqrt(",
    "математика.степень(":      "math.pow(",
    "математика.косинус(":      "math.cos(",
    "математика.синус(":        "math.sin(",
    "математика.пол(":          "math.floor(",
    "математика.потолок(":      "math.ceil(",
    "математика.логарифм(":     "math.log(",

    # random
    "случайный.выбор(":         "random.choice(",
    "случайный.целое(":         "random.randint(",
    "случайный.дробное()":      "random.random()",
    "случайный.перемешать(":    "random.shuffle(",

    # time
    "время.сон(":               "time.sleep(",
    "время.сейчас()":           "time.time()",

    # os
    "ос.путь":                  "os.path",
    "ос.существует(":           "os.path.exists(",
    "ос.создатьПапку(":         "os.mkdir(",
    "ос.удалитьФайл(":          "os.remove(",
    "ос.листДир(":              "os.listdir(",
}


# ═══════════════════════════════════════════════════════════
# 6. ТРАНСЛЯТОР (Ядро RusPy)
# ═══════════════════════════════════════════════════════════

def _extract_strings(line: str):
    """Извлекает строковые литералы, заменяя их на плейсхолдеры.
    Возвращает (строка_с_плейсхолдерами, список_литералов).
    Это нужно, чтобы транслятор НЕ трогал текст внутри кавычек."""
    literals = []
    result = []
    i = 0
    while i < len(line):
        ch = line[i]

        # Проверяем строковые префиксы (f, r, b, F, R, B)
        prefix = ""
        if ch in ('f', 'F', 'r', 'R', 'b', 'B') and i + 1 < len(line) and line[i + 1] in ('"', "'"):
            prefix = ch
            i += 1
            ch = line[i]

        if ch in ('"', "'"):
            # Проверяем тройные кавычки
            if line[i:i+3] in ('"""', "'''"):
                quote = line[i:i+3]
                end = line.find(quote, i + 3)
                if end == -1:
                    end = len(line)
                else:
                    end += 3
            else:
                quote = ch
                end = i + 1
                while end < len(line):
                    if line[end] == '\\':  # Пропускаем экранированные символы
                        end += 2
                        continue
                    if line[end] == quote:
                        end += 1
                        break
                    end += 1
            # Сохраняем литерал (с префиксом) и ставим плейсхолдер
            literal = prefix + line[i:end]
            placeholder = f"__RUSPY_STR_{len(literals)}__"
            literals.append(literal)
            result.append(placeholder)
            i = end
        else:
            result.append(ch)
            i += 1
    return "".join(result), literals


def _restore_strings(line: str, literals: list) -> str:
    """Возвращает строковые литералы на место плейсхолдеров.
    Для f-строк — дополнительно переводит методы внутри {выражений}."""
    for i, lit in enumerate(literals):
        # Если это f-строка, переводим выражения внутри {фигурных скобок}
        if lit.startswith(("f\"", "f'", "F\"", "F'")):
            def _translate_fstring_expr(match):
                expr = match.group(1)
                # Переводим методы внутри выражения
                for rus, eng in sorted(METHODS.items(), key=lambda x: len(x[0]), reverse=True):
                    expr = expr.replace(rus, eng)
                # Переводим встроенные функции
                for rus, eng in sorted(BUILTINS.items(), key=lambda x: len(x[0]), reverse=True):
                    pattern = r'(?<![а-яА-ЯёЁa-zA-Z_0-9])' + re.escape(rus) + r'(?![а-яА-ЯёЁa-zA-Z_])'
                    expr = re.sub(pattern, eng, expr)
                # Переводим сам/себя -> self
                expr = re.sub(r'(?<![а-яА-ЯёЁa-zA-Z_])себя(?![а-яА-ЯёЁa-zA-Z_])', 'self', expr)
                expr = re.sub(r'(?<![а-яА-ЯёЁa-zA-Z_])ам(?![а-яА-ЯёЁa-zA-Z_])', 'self', expr)
                return "{" + expr + "}"
            lit = re.sub(r'\{([^}]+)\}', _translate_fstring_expr, lit)
        line = line.replace(f"__RUSPY_STR_{i}__", lit)
    return line


def translate_line(line: str) -> str:
    """Переводит одну строку с русского на Python."""

    # Сохраняем ведущие пробелы (отступы)
    stripped = line.lstrip()
    indent = line[:len(line) - len(stripped)]

    # Пропускаем пустые строки и комментарии
    if not stripped or stripped.startswith("#") or stripped.startswith("//"):
        if stripped.startswith("//"):
            return indent + "#" + stripped[2:]
        return line

    # --- Фаза 0: Извлекаем строковые литералы (чтобы не переводить текст внутри кавычек) ---
    result, string_literals = _extract_strings(stripped)

    # --- Фаза 1: Магические методы (Dunder) ---
    for rus, eng in DUNDER.items():
        if result.startswith(rus):
            result = result.replace(rus, eng, 1)
            break

    # --- Фаза 2: Ключевые слова ---
    # Используем границы слов для точной замены (включая цифры в lookbehind)
    for rus, eng in sorted(KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r'(?<![а-яА-ЯёЁa-zA-Z_0-9])' + re.escape(rus) + r'(?![а-яА-ЯёЁa-zA-Z_])'
        result = re.sub(pattern, eng, result)

    # --- Фаза 3: Встроенные функции ---
    for rus, eng in sorted(BUILTINS.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r'(?<![а-яА-ЯёЁa-zA-Z_0-9])' + re.escape(rus) + r'(?![а-яА-ЯёЁa-zA-Z_])'
        result = re.sub(pattern, eng, result)

    # --- Фаза 4: Методы ---
    for rus, eng in sorted(METHODS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(rus, eng)

    # --- Фаза 5: Атрибуты модулей ---
    for rus, eng in sorted(MODULE_ATTRS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(rus, eng)

    # --- Фаза 6: Имена модулей в import ---
    for rus, eng in MODULES.items():
        result = result.replace(f"import {rus}", f"import {eng}")
        result = result.replace(f"from {rus}", f"from {eng}")
        pattern = r'(?<![а-яА-ЯёЁa-zA-Z_])' + re.escape(rus) + r'(?=\.)'
        result = re.sub(pattern, eng, result)

    # --- Фаза 7: Замена "//" комментариев на "#" ---
    if "//" in result:
        code_part, _, comment_part = result.partition("//")
        result = code_part + "# " + comment_part

    # --- Фаза 8: Конструкция "себя" -> "self" ---
    result = re.sub(r'(?<![а-яА-ЯёЁa-zA-Z_])себя(?![а-яА-ЯёЁa-zA-Z_])', 'self', result)
    result = re.sub(r'(?<![а-яА-ЯёЁa-zA-Z_])сам(?![а-яА-ЯёЁa-zA-Z_])', 'self', result)

    # --- Фаза 9: Возвращаем строковые литералы на место ---
    result = _restore_strings(result, string_literals)

    return indent + result


def translate_code(source_code: str) -> str:
    """Переводит весь исходный код с русского на Python."""
    lines = source_code.split("\n")
    translated = [translate_line(line) for line in lines]
    return "\n".join(translated)


# ═══════════════════════════════════════════════════════════
# 7. ЗАПУСК ПРОГРАММЫ
# ═══════════════════════════════════════════════════════════

HELP_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║                    🇷🇺 RusPy v1.0 🇷🇺                        ║
║          Транслятор русского синтаксиса в Python             ║
╚══════════════════════════════════════════════════════════════╝

Использование:
    python ruspy.py <файл.рус>              Запустить программу на русском
    python ruspy.py --показать <файл.рус>   Показать сгенерированный Python-код
    python ruspy.py --помощь                Эта справка

Поддерживаемые расширения: .рус, .rus, .1с, .py

Пример файла (программа.рус):
    Сообщить("Привет, мир!")
    
    Функция Приветствие(имя):
        Вернуть "Привет, " + имя + "!"
    
    Если 5 > 3:
        Сообщить(Приветствие("Вася"))
"""


def main():
    args = sys.argv[1:]

    if not args or "--помощь" in args or "--help" in args:
        print(HELP_TEXT)
        return

    show_code = "--показать" in args or "--show" in args
    if show_code:
        args = [a for a in args if a not in ("--показать", "--show")]

    if not args:
        print("❌ Ошибка: Не указан файл для запуска!")
        print("   Использование: python ruspy.py программа.рус")
        return

    filepath = args[0]

    if not os.path.exists(filepath):
        print(f"❌ Ошибка: Файл '{filepath}' не найден!")
        return

    # Читаем исходный код
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    # Переводим
    python_code = translate_code(source)

    if show_code:
        print("=" * 60)
        print("  📝 Сгенерированный Python-код:")
        print("=" * 60)
        for i, line in enumerate(python_code.split("\n"), 1):
            print(f"  {i:3d} | {line}")
        print("=" * 60)
        print()

    # Выполняем
    print("🚀 Запуск RusPy...")
    print("-" * 40)
    try:
        exec(python_code, {"__builtins__": __builtins__, "__name__": "__main__"})
    except Exception as e:
        print(f"\n❌ Ошибка выполнения: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
