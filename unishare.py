import psycopg2
import hashlib

class Student:
    """Клас для роботи з даними студента та авторизацією."""
    def __init__(self, student_id, full_name, email, password_hash):
        self.student_id = student_id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash

    def login(self, entered_password):
        # Перевірка пароля
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        if self.password_hash == entered_hash:
            print(f"Вхід успішний. Вітаємо, {self.full_name}!")
            return True
        print("Помилка авторизації.")
        return False

    def updateProfile(self, new_name, db_connection):
        """Оновлення ПІБ студента через SQL-запит."""
        try:
            cursor = db_connection.cursor()
            update_query = """
                UPDATE students 
                SET full_name = %s 
                WHERE student_id = %s
            """
            cursor.execute(update_query, (new_name, self.student_id))
            db_connection.commit()
            
            self.full_name = new_name
            print(f"Дані оновлено. Поточне ім'я: {self.full_name}")
        except Exception as e:
            print(f"Помилка бази даних: {e}")


class Material:
    """Клас для керування навчальними файлами."""
    def __init__(self, material_id, title, file_path, rating=0.0):
        self.material_id = material_id
        self.title = title
        self.file_path = file_path
        self.rating = rating

    def upload(self, file_size_mb):
        """Перевірка лімітів перед завантаженням."""
        if file_size_mb > 50:
            print(f"Відмовлено: Файл розміром {file_size_mb}MB перевищує ліміт (50MB).")
            return False
        print(f"Файл '{self.title}' успішно завантажено. Очікує перевірки.")
        return True

    def calculateRating(self, new_score):
        """Розрахунок середньої оцінки матеріалу."""
        if 1 <= new_score <= 5:
            self.rating = (self.rating + new_score) / 2
            print(f"Рейтинг файлу '{self.title}' змінено на {self.rating:.1f}")


class Category:
    """Клас для ієрархії дисциплін."""
    def __init__(self, category_id, subject_name, course_year):
        self.category_id = category_id
        self.subject_name = subject_name
        self.course_year = course_year

    def getMaterials(self, db_connection):
        """Отримання списку матеріалів з бази даних."""
        try:
            cursor = db_connection.cursor()
            select_query = """
                SELECT material_id, title, rating 
                FROM materials 
                WHERE category_id = %s 
                ORDER BY rating DESC
            """
            cursor.execute(select_query, (self.category_id,))
            print(f"--- Матеріали для предмету: {self.subject_name} ---")
            for row in cursor.fetchall():
                print(f"ID: {row[0]}, Назва: {row[1]}, Рейтинг: {row[2]}")
        except Exception as e:
            print(f"Помилка завантаження списку: {e}")


# --- Приклад запуску (Тестування логіки) ---
# Симуляція користувача
student_1 = Student(1, "Плахта Андрій", "andriy@unishare.edu.ua", "hash123")

# Симуляція файлу
lab_file = Material(101, "Звіт AI", "/cloud/lab_ai.pdf")

# Симуляція дій
lab_file.upload(12)  # Файл 12 МБ (проходить перевірку)
lab_file.calculateRating(5)
