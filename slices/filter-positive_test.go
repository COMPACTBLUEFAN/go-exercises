package main

import (
	"reflect"
	"testing"
)

func TestFilterPositive(t *testing.T) {
	tests := []struct {
		name string
		nums []int
		want []int
	}{
		{
			name: "Positive numbers",
			nums: []int{1, 2, 3, 4, 5, 6, 7, 8},
			want: []int{1, 2, 3, 4, 5, 6, 7, 8},
		},
		{
			name: "Negative numbers",
			nums: []int{-1, -2, -3, -4, -5, -6, -7, -8},
			want: []int{},
		},
		{
			name: "Mixed numbers",
			nums: []int{1, -2, 3, -4, 5, -6, 7, -8},
			want: []int{1, 3, 5, 7},
		},
		{
			name: "Empty slice",
			nums: []int{},
			want: []int{},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := FilterPositive(tt.nums); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("FilterPositive(%v) = %v; want %v", tt.nums, got, tt.want)
			}
		})
	}
}
