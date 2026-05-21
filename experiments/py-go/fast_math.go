package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	// Создаем сканер для чтения ввода из Python
	scanner := bufio.NewScanner(os.Stdin)
	
	fmt.Println("READY") // Сигнал для Python, что мы запустились

	for scanner.Scan() {
		input := scanner.Text()
		if input == "exit" {
			break
		}

		// Ожидаем два числа через пробел, например "10 20"
		nums := strings.Fields(input)
		if len(nums) != 2 {
			fmt.Println("ERROR: Need 2 numbers")
			continue
		}

		a, _ := strconv.Atoi(nums[0])
		b, _ := strconv.Atoi(nums[1])

		// Отправляем результат обратно в Python
		fmt.Printf("RESULT: %d\n", a+b)
	}
}
