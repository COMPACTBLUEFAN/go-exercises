import subprocess
import os

def main():
    print("--- ЗАПУСК ТРИАДЫ (Python -> Go -> Rust) ---")
    
    # Запускаем Go-оркестратор
    # Используем 'go run', чтобы не мучиться с компиляцией
    process = subprocess.Popen(
        ['go', 'run', 'orchestrator.go'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Ждем готовности оркестратора
    while True:
        line = process.stdout.readline().strip()
        if line == "ORCHESTRATOR_READY":
            print("[Python] Оркестратор Go запущен и ждет!")
            break
        elif line:
            print(f"[Go Logs] {line}")

    while True:
        try:
            val = input("\n[Python] Введите число для расчета факториала (или 'exit'): ")
            if val.lower() == 'exit':
                process.stdin.write("exit\n")
                process.stdin.flush()
                break
            
            # 1. Отправляем в Go
            process.stdin.write(f"{val}\n")
            process.stdin.flush()

            # 2. Получаем результат, который прошел через Rust
            result = process.stdout.readline().strip()
            print(f"[Result] Ответ (через Go и Rust): {result}")

        except KeyboardInterrupt:
            break

    process.terminate()
    print("\n--- ТРИАДА ЗАВЕРШИЛА РАБОТУ ---")

if __name__ == "__main__":
    main()
