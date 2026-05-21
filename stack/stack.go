package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

type Stack struct {
	StSlice []int
}

func (s *Stack) Push(t int) {
	s.StSlice = append(s.StSlice, t)
}

func (s *Stack) Pop() (bool, int) {
	if l := len(s.StSlice); l == 0 {
		return false, 0
	}
	v := len(s.StSlice) - 1
	vq := s.StSlice[v]
	s.StSlice = s.StSlice[:v]
	return true, vq
}

func main() {
	mode := flag.String("mode", "push", "push, pop")
	flag.Parse()
	scanner := bufio.NewScanner(os.Stdin)
	leng := len(flag.Args())
	s := Stack{}
	if *mode == "push" {
		if leng == 0 {
			fmt.Println("Number: ")
			scanner.Scan()
			ternumtxt := scanner.Text()
			ternum, _ := strconv.Atoi(ternumtxt)
			s.Push(ternum)
		}
		if leng == 1 {
			num, _ := strconv.Atoi(flag.Args()[0])
			s.Push(num)
		}
		if leng > 1 {
			fmt.Println("Too many numbers. Only one int can be pushed at the time")
		}
	}
	if *mode == "pop" {
		if len(s.StSlice) == 0 {
			fmt.Println("Stack is empty")
			return
		} else {
			bo, nump := s.Pop()
			fmt.Printf("Status: %v. Number: %d\n", bo, nump)
		}
	}
}
