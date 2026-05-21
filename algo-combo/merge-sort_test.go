package main

import "testing"

func TestMergeSort(t *testing.T) {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	expected := []int{3, 9, 10, 27, 38, 43, 82}

	result := MergeSort(arr)

	if len(result) != len(expected) {
		t.Fatalf("Got length %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("At index %d: got %d, want %d", i, v, expected[i])
		}
	}
}

func TestBinarySearch(t *testing.T) {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	arr = MergeSort(arr) // Обязательная сортировка перед бинарным поиском!

	result := BinarySearch(arr, 27)

	if result != 3 {
		t.Errorf("Got index %d, want %d", result, 3)
	}
}
