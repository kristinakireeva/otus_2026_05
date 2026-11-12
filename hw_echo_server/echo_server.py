import argparse
from http import HTTPStatus
import socket
from urllib.parse import parse_qs, urlparse


def get_status_phrase(status_code: int) -> str:
    """Возвращает стандартную фразу для HTTP-статуса через модуль http."""
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return ""


def resolve_status(raw_path: str) -> tuple[int, str]:
    """Извлекает GET-параметр status и возвращает валидный код и фразу."""
    parsed_url = urlparse(raw_path)
    query_params = parse_qs(parsed_url.query)

    status_values = query_params.get("status")
    if not status_values:
        return 200, "OK"

    first_status = next(iter(status_values), "")
    try:
        code = int(first_status)
        phrase = get_status_phrase(code)
        if phrase:
            return code, phrase
    except ValueError:
        pass

    return 200, "OK"


def parse_http_request(raw_data: str) -> tuple[str, str, list[tuple[str, str]]]:
    """Разбирает сырой HTTP-запрос на метод, путь и список заголовков."""
    header_section, *_ = raw_data.split("\r\n\r\n", 1)
    lines = header_section.split("\r\n")

    if not lines:
        return "GET", "/", []

    first_line, *header_lines = lines
    request_line_parts = first_line.split()

    if len(request_line_parts) >= 2:
        method, path, *_ = request_line_parts
    elif len(request_line_parts) == 1:
        method = next(iter(request_line_parts))
        path = "/"
    else:
        method, path = "GET", "/"

    headers = []
    for line in header_lines:
        if ":" in line:
            name, value = line.split(":", 1)
            headers.append((name.strip(), value.strip()))

    return method, path, headers


def build_response(
    method: str,
    client_addr: tuple[str, int],
    status_code: int,
    status_phrase: str,
    headers: list[tuple[str, str]],
) -> bytes:
    """Формирует валидный HTTP-ответ со всей требуемой информацией."""
    body_lines = [
        f"Request Method: {method}",
        f"Request Source: {client_addr}",
        f"Response Status: {status_code} {status_phrase}",
    ]

    for name, value in headers:
        body_lines.append(f"{name}: {value}")

    body = "\r\n".join(body_lines)
    body_bytes = body.encode("utf-8")

    response_headers = [
        f"HTTP/1.1 {status_code} {status_phrase}",
        "Content-Type: text/plain; charset=utf-8",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
        "",
        "",
    ]
    header_bytes = "\r\n".join(response_headers).encode("utf-8")

    return header_bytes + body_bytes


def run_server(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Запускает цикл обработки входящих TCP-соединений."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Echo-сервер запущен на http://{host}:{port}")

        while True:
            conn, client_addr = server_socket.accept()
            with conn:
                raw_bytes = conn.recv(4096)
                if not raw_bytes:
                    continue

                raw_text = raw_bytes.decode("utf-8", errors="replace")
                method, path, headers = parse_http_request(raw_text)
                status_code, status_phrase = resolve_status(path)

                response_bytes = build_response(
                    method=method,
                    client_addr=client_addr,
                    status_code=status_code,
                    status_phrase=status_phrase,
                    headers=headers,
                )
                conn.sendall(response_bytes)


def main():
    parser = argparse.ArgumentParser(description="HTTP Echo Server на сокетах")
    parser.add_argument("--host", default="127.0.0.1", help="Хост сервера")
    parser.add_argument("--port", type=int, default=5000, help="Порт сервера")
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
