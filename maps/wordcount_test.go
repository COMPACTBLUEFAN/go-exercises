package main

import (
	"reflect"
	"testing"
)

func TestWordCount(t *testing.T) {
	tests := []struct {
		name string
		text string
		want map[string]int
	}{
		{
			name: "Positive numbers",
			text: "1 2 3 4 5 6 7 8",
			want: map[string]int{"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1},
		},
		{
			name: "Negative numbers",
			text: "-1 -2 -3 -4 -5 -6 -7 -8",
			want: map[string]int{"-1": 1, "-2": 1, "-3": 1, "-4": 1, "-5": 1, "-6": 1, "-7": 1, "-8": 1},
		},
		{
			name: "Mixed numbers",
			text: "1 -2 3 -4 5 -6 7 -8",
			want: map[string]int{"1": 1, "-2": 1, "3": 1, "-4": 1, "5": 1, "-6": 1, "7": 1, "-8": 1},
		},
		{
			name: "Empty slice",
			text: "",
			want: map[string]int{},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := WordCount(tt.text); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("WordCount(%v) = %v; want %v", tt.text, got, tt.want)
			}
		})
	}
}
