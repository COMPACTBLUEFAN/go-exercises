package main

import "fmt"

type LogEntry struct {
	Level   string // "INFO", "WARN", "ERROR"
	Message string
	Line    int
}

// FilterByLevel возвращает только записи с указанным уровнем
func FilterByLevel(entries []LogEntry, level string) []LogEntry {
	var a []LogEntry
	for _, entry := range entries {
		if entry.Level == level {
			a = append(a, entry)
		}
	}
	return a
}

// CountByLevel возвращает map[string]int с количеством записей каждого уровня
func CountByLevel(entries []LogEntry) map[string]int {
	entriesmap := make(map[string]int)
	for _, entry := range entries {
		entriesmap[entry.Level]++
	}
	return entriesmap
}

func main() {
	logs := []LogEntry{
		{"INFO", "Server started", 1},
		{"ERROR", "Connection refused", 15},
		{"WARN", "Slow query", 42},
		{"ERROR", "Timeout", 78},
		{"INFO", "Request handled", 100},
	}

	errors := FilterByLevel(logs, "ERROR")
	fmt.Println("Errors:", errors)

	stats := CountByLevel(logs)
	fmt.Println("Stats:", stats)
}
