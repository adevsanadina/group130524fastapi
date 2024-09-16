import sqlite3
from fastapi import HTTPException, status
from schemas import NewTour, SavedTour


class StorageSQLite:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.tour_table_name = 'tours'
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                CREATE TABLE IF NOT EXISTS {self.tour_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    destination TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(query)

    def create_tour(self, new_tour: NewTour) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = (new_tour.title, new_tour.description, new_tour.price, new_tour.destination)
            query = f"""
                INSERT INTO {self.tour_table_name} (title, description, price, destination)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, values)
        return self._get_latest_tour()

    def _get_latest_tour(self) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, destination, created_at
                FROM {self.tour_table_name}
                ORDER BY id DESC
                LIMIT 1
            """
            result: tuple = cursor.execute(query).fetchone()
            return SavedTour(
                id=result[0], title=result[1], description=result[2], price=result[3], destination=result[4], created_at=result[5]
            )

    def get_tour(self, _id: int) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, destination, created_at
                FROM {self.tour_table_name}
                WHERE id = ?
            """
            result = cursor.execute(query, (_id,)).fetchone()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tour with id {_id} not found')
            return SavedTour(id=result[0], title=result[1], description=result[2], price=result[3], destination=result[4], created_at=result[5])

    def get_tours(self, limit: int = 10, q: str = '') -> list[SavedTour]:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, destination, created_at
                FROM {self.tour_table_name}
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY id DESC
                LIMIT ?
            """
            data = cursor.execute(query, (f'%{q}%', f'%{q}%', limit)).fetchall()
        return [SavedTour(id=row[0], title=row[1], description=row[2], price=row[3], destination=row[4], created_at=row[5]) for row in data]

    def update_tour_price(self, _id: int, new_price: float) -> SavedTour:
        self.get_tour(_id)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"UPDATE {self.tour_table_name} SET price = ? WHERE id = ?"
            cursor.execute(query, (new_price, _id))
        return self.get_tour(_id)

    def delete_tour(self, _id: int):
        self.get_tour(_id)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"DELETE FROM {self.tour_table_name} WHERE id = ?"
            cursor.execute(query, (_id,))


storage = StorageSQLite('db_tours.sqlite')


