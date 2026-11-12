import argparse
from collections import Counter
import json
import os
import re

# Регулярное выражение для быстрого и точного разбора строки лога
LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "(?P<request>[^"]*)" '
    r'\d+ \S+ "[^"]*" "[^"]*" (?P<duration>\d+)$'
)

TARGET_METHODS = ("GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD")


def parse_log_file(filepath: str) -> dict:
    """Анализирует один лог-файл за один проход и возвращает статистику."""
    total_requests = 0
    methods_count = {method: 0 for method in TARGET_METHODS}
    ip_counts = Counter()
    top_longest = []  # Список кортежей: (duration, index, request_info)

    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        for line_idx, line in enumerate(file):
            line = line.strip()
            if not line:
                continue

            total_requests += 1
            match = LOG_PATTERN.match(line)
            if not match:
                continue

            ip = match.group("ip")
            dt = match.group("datetime")
            request = match.group("request")
            duration = int(match.group("duration"))

            ip_counts[ip] += 1

            # Разбираем строку запроса вида "GET /index.php HTTP/1.1"
            req_parts = request.split()
            method = req_parts[0] if len(req_parts) >= 1 else ""
            url = req_parts[1] if len(req_parts) >= 2 else ""

            if method in methods_count:
                methods_count[method] += 1

            # Поддерживаем актуальный топ-3 самых долгих запросов без хранения всех 3 млн строк
            if len(top_longest) < 3 or duration > top_longest[-1][0]:
                req_info = {
                    "method": method,
                    "url": url,
                    "ip": ip,
                    "duration": duration,
                    "datetime": dt,
                }
                # Отрицательный line_idx сохраняет порядок появления при равной длительности
                top_longest.append((duration, -line_idx, req_info))
                top_longest.sort(key=lambda item: (item[0], item[1]), reverse=True)
                if len(top_longest) > 3:
                    top_longest.pop()

    top_ips = [
        {"ip": ip, "count": count} for ip, count in ip_counts.most_common(3)
    ]

    longest_requests = [item[2] for item in top_longest]

    return {
        "file": os.path.basename(filepath),
        "total_requests": total_requests,
        "methods": methods_count,
        "top_3_ips": top_ips,
        "top_3_longest_requests": longest_requests,
    }


def process_path(target_path: str) -> None:
    """Определяет файл или директорию и запускает обработку."""
    files_to_process = []

    if os.path.isfile(target_path):
        files_to_process.append(target_path)
    elif os.path.isdir(target_path):
        for entry in sorted(os.listdir(target_path)):
            full_path = os.path.join(target_path, entry)
            # Обрабатываем только файлы, игнорируя вложенные папки и уже созданные json-отчеты
            if os.path.isfile(full_path) and not entry.endswith(".json"):
                files_to_process.append(full_path)
    else:
        print(f"Ошибка: путь '{target_path}' не найден.")
        return

    if not files_to_process:
        print(f"В директории '{target_path}' не найдено файлов для анализа.")
        return

    for filepath in files_to_process:
        print(f"Обработка файла: {filepath} ...")
        stats = parse_log_file(filepath)

        # Вывод результата в терминал
        output_json = json.dumps(stats, ensure_ascii=False, indent=4)
        print(output_json)
        print("-" * 50)

        # Сохранение в отдельный JSON-файл рядом с исходным логом
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_filename = f"{base_name}_stats.json"
        output_path = os.path.join(os.path.dirname(filepath), output_filename)

        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(output_json + "\n")

        print(f"Статистика сохранена в файл: {output_path}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Парсер логов веб-сервера (формат access.log)."
    )
    parser.add_argument(
        "path",
        help="Путь к конкретному лог-файлу или к директории с лог-файлами",
    )
    args = parser.parse_args()
    process_path(args.path)


if __name__ == "__main__":
    main()
