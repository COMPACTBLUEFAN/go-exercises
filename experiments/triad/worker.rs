use std::io::{self, BufRead};

fn factorial(n: u64) -> u64 {
    if n == 0 { 1 } else { n * factorial(n - 1) }
}

fn main() {
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        if let Ok(input) = line {
            let val = input.trim();
            if val == "exit" { break; }

            // Пытаемся превратить строку в число
            match val.parse::<u64>() {
                Ok(n) if n <= 20 => {
                    println!("{}", factorial(n));
                }
                Ok(_) => {
                    println!("ERROR: Number too big (max 20)");
                }
                Err(_) => {
                    println!("ERROR: Invalid input");
                }
            }
        }
    }
}
