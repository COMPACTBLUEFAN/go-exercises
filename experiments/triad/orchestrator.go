package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("./worker.exe")

	rustStdin, _ := cmd.StdinPipe()
	rustStdout, _ := cmd.StdoutPipe()
	
	if err := cmd.Start(); err != nil {
		fmt.Println("ORCHESTRATOR_ERROR: Could not start Rust worker")
		return
	}

	pyScanner := bufio.NewScanner(os.Stdin)
	rustScanner := bufio.NewScanner(rustStdout)

	fmt.Println("ORCHESTRATOR_READY")

	for pyScanner.Scan() {
		input := pyScanner.Text()
		if input == "exit" {
			break
		}

		// Отправляем в Rust
		fmt.Fprintln(rustStdin, input)

		// Ждем ответ. Если Scan() вернул false — значит Rust закрылся или упал
		if rustScanner.Scan() {
			result := rustScanner.Text()
			fmt.Printf("FINAL_RESULT: %s\n", result)
		} else {
			fmt.Println("FINAL_RESULT: [Error] Worker disconnected or crashed")
		}
	}

	cmd.Process.Kill()
}
