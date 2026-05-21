package main

import "fmt"

type Formatter interface {
	Format() string
}

type LogEntry struct {
	Level   string // "INFO", "WARN", "ERROR"
	Message string
	Line    int
}

func (l LogEntry) Format() string {
	return fmt.Sprintf("[%s] L%d: %s", l.Level, l.Line, l.Message)
}

func (l LogEntry) String() string {
	return fmt.Sprintf("🔥 [%s] Line %d: %s (Self-printing!)", l.Level, l.Line, l.Message)
}

type User struct {
	Name string
	Role string
}

func (u User) Format() string {
	return fmt.Sprintf("User: %s (%s)", u.Name, u.Role)
}

type Error struct {
	Code int
	Message string
}

func (e Error) Format() string {
	return fmt.Sprintf("Code: %d \n%s", e.Code, e.Message)
}

func Report(f Formatter) {
	fmt.Println(f.Format())
}

func main() {
	var f Formatter
	f = LogEntry{
		Level:   "INFO",
		Message: "User logged in",
		Line:    10,
	}
	Report(f)
	fmt.Println(f)
	f = User{
		Name: "John",
		Role: "admin",
	}
	Report(f)
	f = Error{
		Code: 404,
		Message: "Not Found",
	}
	Report(f)
}
