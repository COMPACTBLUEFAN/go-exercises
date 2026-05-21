package main

var s []int

var ch1 = make(chan int, 2)

func ConcurrentSum(s []int) int {
	fhs := s[:len(s)/2]
	shs := s[len(s)/2:]
	go func() {
		fhsSum := 0
		for _, i := range fhs {
			fhsSum += i
		}
		ch1 <- fhsSum
	}()
	go func() {
		shsSum := 0
		for _, i := range shs {
			shsSum += i
		}
		ch1 <- shsSum
	}()
	x := <-ch1 + <-ch1
	return x
}
