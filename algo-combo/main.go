package main

func MergeSort(array []int) []int {
	if len(array) <= 1 {
		return array
	}
	mid := len(array) / 2
	left := MergeSort(array[:mid])
	right := MergeSort(array[mid:])
	return merge(left, right)
}

func merge(left, right []int) []int {
	result := make([]int, 0, len(left)+len(right))
	l, r := 0, 0

	for l < len(left) && r < len(right) {
		if left[l] < right[r] {
			result = append(result, left[l])
			l++
		} else {
			result = append(result, right[r])
			r++
		}
	}

	// Append remaining elements from both slices
	result = append(result, left[l:]...)
	result = append(result, right[r:]...)

	return result
}

func BinarySearch(sortedArray []int, target int) int {
	if len(sortedArray) == 0 {
		return -1
	}

	mid := len(sortedArray) / 2

	if sortedArray[mid] == target {
		return mid
	}

	if sortedArray[mid] < target {
		// Ищем в правой части (нужен сдвиг индекса)
		res := BinarySearch(sortedArray[mid+1:], target)
		if res == -1 {
			return -1
		}
		return mid + 1 + res
	}

	// Ищем в левой части
	return BinarySearch(sortedArray[:mid], target)
}
