import subprocess

def main():
    # 1. Запускаем нашего Go-посланника
    # Мы используем 'go run', чтобы не компилировать каждый раз
    process = subprocess.Popen(
        ['go', 'run', 'fast_math.go'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True, # Работаем с текстом, а не байтами
        bufsize=1  # Строковая буферизация
    )

    print("[Python] Ожидаю готовности Go...")
    
    # Читаем первую строку от Go (сигнал READY)
    ready = process.stdout.readline().strip()
    if ready == "READY":
        print("[Python] Go готов! Отправляю задачу...")
        
        # 2. Отправляем числа в Go (через стандартный ввод)
        process.stdin.write("125 75\n")
        process.stdin.flush() # Принудительно проталкиваем данные в трубу

        # 3. Получаем ответ
        result = process.stdout.readline().strip()
        print(f"[Python] Получен ответ от Go: {result}")

        # Завершаем работу
        process.stdin.write("exit\n")
        process.stdin.flush()
    else:
        print(f"[Python] Что-то пошло не так: {ready}")

    process.wait()
    print("[Python] Работа завершена.")

if __name__ == "__main__":
    main()
