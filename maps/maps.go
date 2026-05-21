package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func WordCount(text string) map[string]int {
	words := strings.Fields(text)
	WordMap := make(map[string]int)

	for _, word := range words {
		WordMap[word]++
	}
	return WordMap
}

func main() {
	fmt.Println("Lemme check how often you do repeat words\n Just text me smth")
	scanner := bufio.NewScanner(os.Stdin)
	var text string
	if scanner.Scan() {
		text = scanner.Text()
	}
	out := WordCount(text)
	fmt.Println(out)
	fmt.Println("Repeated words:")
	if text == "" {
		fmt.Println("You didn't text me anything, bro")
	}
	for word, count := range out {
		if count > 1 {
			fmt.Println(word)
		}
	}
	fmt.Println("Unique words:")
	for word, count := range out {
		if count == 1 {
			fmt.Println(word)
		}
	}
	for word, count := range out {
		if count > 5 {
			fmt.Println(word)
			fmt.Println("And this is ace, right?")
		}
	}
	if text == "Nedojun" {
		fmt.Println("Oh, hi Maks!")
	}
}
