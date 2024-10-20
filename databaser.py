import sqlite3, json
from typing import Dict, List

class Databaser:
    def __init__(self, db_name: str = 'database.db'):
        """Initialize the database connection."""
        try:
            print('\n[Database] | Инициализация базы данных!\n')
            self.connection = sqlite3.connect(db_name, check_same_thread=False, timeout=7)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT,
                                level INTEGER,
                                language  TEXT,
                                phone TEXT UNIQUE)''')
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка базы данных: {e}\n')
            raise
        else:
            print('\n[Database] | База данных загружена!\n')

    def remove_user_by_id(self, id: int) -> None:
        """Remove a user by ID."""
        try:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка удаления пользователя: {e}\n')
            raise

    def remove_user(self, phone: str) -> None:
        """Remove a user by phone."""
        try:
            self.cursor.execute('DELETE FROM users WHERE phone = ?', (phone,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка удаления пользователя: {e}\n')
            raise

    def add_user(self, name: str, language: str, phone: str):
        """Add a new user."""
        try:
            # Update the user's information
            self.connection.execute("""INSERT INTO users (name, language, level, phone) VALUES (?, ?, ?, ?)""", [name, language, '1', phone])

            # Commit the transaction
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка добавления пользователя: {e}\n')
            raise

    def set_user_level(self, level: str, phone: str):
        try:
            # Update the user's level
            self.connection.execute("""UPDATE users SET level = ? WHERE phone = ?""", [level, phone])

            # Commit the transaction
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка обновления уровня пользователя: {e}\n')
            raise


    def set_user_language(self, language: str, phone: str):
        try:
            self.connection.execute("""UPDATE users SET (language) VALUES (?) WHERE phone = ?""", [language, phone])

            # Commit the transaction
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка добавления пользователя: {e}\n')
            raise

    def get_user_language(self, phone: str):
        try:
            self.cursor.execute('SELECT language FROM users WHERE phone = ?', (phone,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка добавления пользователя: {e}\n')
            raise

    def get_user(self, phone):
        try:
            self.cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
            user_data = self.cursor.fetchone()
            return user_data
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка получения пользователя: {e}\n')
            raise
        
    def get_user_name(self, phone: str) -> str:
        """Get user name from the users table."""
        try:
            self.cursor.execute('SELECT name FROM users WHERE phone = ?', (phone,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка получения имени пользователя: {e}\n')
            raise

    def get_user_level(self, phone: str):
        """Get user last name from the users table."""
        try:
            self.cursor.execute('SELECT level FROM users WHERE phone = ?', (phone,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f'\n[Database] | Ошибка получения фамилии пользователя: {e}\n')
            raise

if __name__ == '__main__':
    pass