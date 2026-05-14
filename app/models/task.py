import sqlite3
import os

# Define the database path
# Using an absolute path or relative to the project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳一個資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以用 dict 欄位存取
    return conn

class TaskModel:
    @staticmethod
    def get_all(status=None):
        """取得所有任務。可選用 status (0 或 1) 過濾"""
        conn = get_db_connection()
        try:
            if status is not None:
                tasks = conn.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,)).fetchall()
            else:
                tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
            return tasks
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id):
        """依 ID 取得單筆任務"""
        conn = get_db_connection()
        try:
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            return task
        finally:
            conn.close()

    @staticmethod
    def create(title, description=None):
        """新增一筆任務"""
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO tasks (title, description) VALUES (?, ?)',
                (title, description)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def update(task_id, title, description=None):
        """更新指定任務的標題與描述"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE tasks SET title = ?, description = ? WHERE id = ?',
                (title, description, task_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def toggle_status(task_id):
        """切換指定任務的完成狀態 (0 變 1, 1 變 0)"""
        conn = get_db_connection()
        try:
            # 取得目前的狀態
            task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
            if task is None:
                return False
            
            new_status = 0 if task['status'] == 1 else 1
            conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete(task_id):
        """刪除指定的任務"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        finally:
            conn.close()
