import os
import sys
import pymysql
import pytest

# Добавляем текущую директорию в sys.path, чтобы импорт from lib.db работал при любом способе запуска pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def pytest_addoption(parser):
    parser.addoption("--host", default="127.0.0.1", help="MySQL host")
    parser.addoption("--port", type=int, default=3306, help="MySQL port")
    parser.addoption("--database", default="bitnami_prestashop", help="MySQL database name")
    parser.addoption("--user", default="bn_prestashop", help="MySQL user")
    parser.addoption("--password", default="", help="MySQL password")


@pytest.fixture(scope="session")
def connection(request):
    host = request.config.getoption("--host")
    port = request.config.getoption("--port")
    database = request.config.getoption("--database")
    user = request.config.getoption("--user")
    password = request.config.getoption("--password")

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
    )
    yield conn
    conn.close()
