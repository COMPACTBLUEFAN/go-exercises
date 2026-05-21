package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

var result []int
var wg sync.WaitGroup
var mu sync.Mutex

func filterPositive(s []int) []int {
	for _, v := range s {
		wg.Go(func() {
			if v > 0 {
				mu.Lock()
				defer mu.Unlock()
				result = append(result, v)
			}
		})
	}
	wg.Wait()
	return result
}

func main() {
	fmt.Println("What you want, user?")
	fmt.Println("1. Filter positive numbers")
	fmt.Println("2. Concurrent sum")
	fmt.Println("3. Exit")
	choice := bufio.NewScanner(os.Stdin)
	choice.Scan()
	switch ChoiceText := choice.Text(); ChoiceText {
	case "1", "Filter positive numbers":
		fmt.Println("Enter numbers separated by spaces")
		choice.Scan()
		NumbersText := choice.Text()
		for _, i := range strings.Fields(NumbersText) {
			integers, _ := strconv.Atoi(i)
			s = append(s, integers)
		}
		fmt.Println(filterPositive(s))
	case "2", "Concurrent sum":
		fmt.Println("Enter numbers separated by spaces")
		choice.Scan()
		NumbersText := choice.Text()
		for _, i := range strings.Fields(NumbersText) {
			integers, _ := strconv.Atoi(i)
			s = append(s, integers)
		}
		fmt.Println(ConcurrentSum(s))
	case "3", "Exit":
		return
	default:
		fmt.Println("Invalid choice")
	}
}
