# РЕШЕНИЕ ДЗ ЗА 27.04.2026

## Функция FilterByLevel

```go
func FilterByLevel(entries []LogEntry, level string) []LogEntry {
	var a []LogEntry
	for _, entry := range entries {
		if entry.Level == level {
			a = append(a, entry)
		}
	}
	return a
}
```

**Объяснение:**

1. `var a []LogEntry` - объявляем пустой срез (slice) типа `LogEntry`, в который будем складывать найденные записи.
2. `for _, entry := range entries` - проходим в цикле по всем записям в переданном срезе `entries`. `_` используется, так как индекс нам не важен.
3. `if entry.Level == level` - проверяем, совпадает ли уровень текущей записи (`entry.Level`) с искомым уровнем (`level`).
4. `a = append(a, entry)` - если уровни совпадают, добавляем текущую запись `entry` в срез `a`.
5. `return a` - возвращаем отфильтрованный срез.

## Функция CountByLevel

```go
func CountByLevel(entries []LogEntry) map[string]int {
	entriesmap := make(map[string]int)
	for _, entry := range entries {
		entriesmap[entry.Level]++
	}
	return entriesmap
}
```

**Объяснение:**

1. `entriesmap := make(map[string]int)` - создаем пустую карту (map) с ключами типа `string` (уровень лога) и значениями типа `int` (количество).
2. `for _, entry := range entries` - проходим в цикле по всем записям в переданном срезе `entries`.
3. `entriesmap[entry.Level]++` - используем уровень текущей записи (`entry.Level`) как ключ в карте. Оператор `++` увеличивает значение по этому ключу на 1. Если ключ встречается впервые, он создается автоматически со значением 1.
4. `return entriesmap` - возвращаем карту с подсчитанными уровнями.
