package main

import "testing"

func TestSum(t *testing.T) {
	nums := []int{1, 2, 3, 4, 5, 6, 7, 8}
	if Sum(nums) != 36 {
		t.Errorf("Sum(%v) = %d; want %d", nums, Sum(nums), 36)
	}
}
