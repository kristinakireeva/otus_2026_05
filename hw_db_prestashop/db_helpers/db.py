from datetime import datetime
import uuid
import pymysql


def create_customer(connection, customer_data: dict) -> int:
    """Создает нового клиента в таблице ps_customer и возвращает его id_customer."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    default_values = {
        "id_shop_group": 1,
        "id_shop": 1,
        "id_gender": 1,
        "id_default_group": 3,
        "id_lang": 1,
        "id_risk": 0,
        "firstname": "Test",
        "lastname": "User",
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "passwd": "hashed_password_example_123456",
        "last_passwd_gen": now,
        "birthday": "1990-01-01",
        "newsletter": 0,
        "optin": 0,
        "active": 1,
        "is_guest": 0,
        "deleted": 0,
        "secure_key": uuid.uuid4().hex,
        "date_add": now,
        "date_upd": now,
    }
    data = {**default_values, **customer_data}

    columns = ", ".join(f"`{key}`" for key in data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO `ps_customer` ({columns}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(sql, tuple(data.values()))
        customer_id = cursor.lastrowid
    connection.commit()
    return customer_id


def get_customer_by_id(connection, customer_id: int) -> dict | None:
    """Возвращает данные клиента по id_customer или None, если клиент не найден."""
    sql = "SELECT * FROM `ps_customer` WHERE `id_customer` = %s"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def update_customer(connection, customer_id: int, update_data: dict) -> int:
    """Обновляет поля клиента по id_customer. Возвращает количество затронутых строк."""
    if not update_data:
        return 0

    update_data_with_time = {
        **update_data,
        "date_upd": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    set_clause = ", ".join(f"`{key}` = %s" for key in update_data_with_time.keys())
    sql = f"UPDATE `ps_customer` SET {set_clause} WHERE `id_customer` = %s"

    params = list(update_data_with_time.values()) + [customer_id]
    with connection.cursor() as cursor:
        affected_rows = cursor.execute(sql, params)
    connection.commit()
    return affected_rows


def delete_customer(connection, customer_id: int) -> int:
    """Удаляет клиента из таблицы ps_customer. Возвращает количество удаленных строк."""
    sql = "DELETE FROM `ps_customer` WHERE `id_customer` = %s"
    with connection.cursor() as cursor:
        affected_rows = cursor.execute(sql, (customer_id,))
    connection.commit()
    return affected_rows
