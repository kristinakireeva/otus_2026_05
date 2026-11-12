from collections import Counter
from datetime import datetime
import subprocess


def parse_ps_aux() -> str:
    result = subprocess.run(
        ["ps", "aux"], capture_output=True, text=True, check=True
    )

    lines = result.stdout.strip().splitlines()
    process_lines = lines[1:]

    total_processes = len(process_lines)
    user_counts = Counter()
    total_cpu = 0.0
    total_mem = 0.0

    max_mem = -1.0
    max_mem_process = ""

    max_cpu = -1.0
    max_cpu_process = ""

    for line in process_lines:
        # maxsplit=10 гарантирует, что колонка COMMAND (индекс 10) не разобьется по пробелам
        parts = line.split(maxsplit=10)
        if len(parts) < 11:
            continue

        user = parts[0]
        cpu = float(parts[2])
        mem = float(parts[3])
        command = parts[10]

        user_counts[user] += 1
        total_cpu += cpu
        total_mem += mem

        if mem > max_mem:
            max_mem = mem
            max_mem_process = command[:20]

        if cpu > max_cpu:
            max_cpu = cpu
            max_cpu_process = command[:20]

    users_formatted = ", ".join(f"'{user}'" for user in user_counts.keys())

    user_processes_lines = [
        f"{user}: {count}" for user, count in user_counts.most_common()
    ]
    user_processes_block = "\n".join(user_processes_lines)

    report = (
        f"Отчёт о состоянии системы:\n"
        f"Пользователи системы: {users_formatted}\n"
        f"Процессов запущено: {total_processes}\n\n"
        f"Пользовательских процессов:\n"
        f"{user_processes_block}\n\n"
        f"Всего памяти используется: {total_mem:.1f}%\n"
        f"Всего CPU используется: {total_cpu:.1f}%\n"
        f"Больше всего памяти использует: {max_mem_process}\n"
        f"Больше всего CPU использует: {max_cpu_process}"
    )

    return report


def main():
    report = parse_ps_aux()

    print(report)

    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report + "\n")


if __name__ == "__main__":
    main()
