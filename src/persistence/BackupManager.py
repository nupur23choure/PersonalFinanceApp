import shutil
import os

class BackupManager:
    def __init__(self, database_path, backup_dir):
        self.database_path = database_path
        self.backup_dir = backup_dir

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        self.backup_path = os.path.join(self.backup_dir, 'users_backup.db')

    def backup_database(self):
        try:
            shutil.copy(self.database_path, self.backup_path)
            print(f"Database backup successful. Backup stored at {self.backup_path}")
        except Exception as e:
            print(f"Error backing up database: {e}")

    def restore_database(self):
        try:
            shutil.copy(self.backup_path, self.database_path)
            print(f"Database restoration successful. Database restored from {self.backup_path}")
        except Exception as e:
            print(f"Error restoring database: {e}")
