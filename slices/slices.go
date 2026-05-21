package main

import (
	"fmt"
	"slices"
)

func Sum(nums []int) int {
	total := 0
	for _, v := range nums {
		total += v
	}
	return total
}

func FilterPositive(nums []int) []int {
	ps := make([]int, 0, len(nums))
	for _, v := range nums {
		if v > 0 {
			ps = append(ps, v)
		}

	}
	if len(ps) > 0 && (len(nums)/len(ps) >= 2 || len(nums)-len(ps) > 50) {
		ps = slices.Clip(ps)
	}
	return ps
}

func main() {
	var slice []int
	fmt.Println("You're welcome in slices!\nInput any letter to run\n\nInput numbers: ")
	for {
		var temp int
		_, err := fmt.Scan(&temp)
		if err != nil {
			break
		}
		slice = append(slice, temp)
	}
	fmt.Println("Sum of your numbers is", Sum(slice))
	fmt.Println("These of your numbers were positive:", FilterPositive(slice))
	if len(slice) > 50 {
		fmt.Println("Bro, you're typing too much fr")
	} else {
		fmt.Println("Pretty easy to calculate, right?")
	}

}
