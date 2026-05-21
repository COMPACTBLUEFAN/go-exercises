package main

import (
	"fmt"
	"os"
	"strconv"
)

// ping отправляет мяч в pich и ждет ответ из poch
func ping(pich, poch, quit chan string, iter int) {
	for i := 0; i < iter; i++ {
		pich <- "ping"      // Бросаем
		fmt.Println(<-poch) // Ждем ответ и печатаем его
	}
	quit <- "done" // Сигналим мэйну, что закончили
}

// pong ждет мяч из pich и отправляет ответ в poch
func pong(pich, poch chan string, iter int) {
	for i := 0; i < iter; i++ {
		fmt.Println(<-pich) // Печатаем "ping"
		poch <- "pong"      // Отбиваем
	}
}

func main() {
	pich := make(chan string)
	poch := make(chan string)
	quit := make(chan string)

	if len(os.Args) == 1 {
		fmt.Println("Usage: go run pingpong.go <number>")
		return
	}

	iterations, err := strconv.Atoi(os.Args[1]) // ТВОЯ ПЕРЕМЕННАЯ ТУТ

	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	go ping(pich, poch, quit, iterations)
	go pong(pich, poch, iterations)

	fmt.Println(<-quit) // Ждем, пока кто-то напишет в quit
}
