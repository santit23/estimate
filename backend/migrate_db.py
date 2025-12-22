import sqlite3
import os

DB_FILE = "sql_app.db"

def migrate():
    if not os.path.exists(DB_FILE):
        print("Database not found, skipping migration.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(material_rates)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "color" not in columns:
            print("Adding color column to material_rates...")
            cursor.execute("ALTER TABLE material_rates ADD COLUMN color VARCHAR DEFAULT 'mill'")
            conn.commit()
            print("Color column already exists in material_rates.")
            
        if "unit" not in columns:
            print("Adding unit column to material_rates...")
            cursor.execute("ALTER TABLE material_rates ADD COLUMN unit VARCHAR")
            conn.commit()
            
        if "category" not in columns:
            print("Adding category column to material_rates...")
            cursor.execute("ALTER TABLE material_rates ADD COLUMN category VARCHAR DEFAULT 'other'")
            conn.commit()
        else:
            print("Color column already exists in material_rates.")
            
        # Check estimate_items table
        cursor.execute("PRAGMA table_info(estimate_items)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "color" not in columns:
            print("Adding color column to estimate_items...")
            cursor.execute("ALTER TABLE estimate_items ADD COLUMN color VARCHAR DEFAULT 'mill'")
            conn.commit()
            
        if "is_active" not in columns:
            print("Adding is_active column to estimate_items...")
            cursor.execute("ALTER TABLE estimate_items ADD COLUMN is_active BOOLEAN DEFAULT 1")
            conn.commit()

        # Check estimates table
        cursor.execute("PRAGMA table_info(estimates)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "transport_cost" not in columns:
            print("Adding transport_cost column to estimates...")
            cursor.execute("ALTER TABLE estimates ADD COLUMN transport_cost FLOAT DEFAULT 0.0")
            conn.commit()
            
        if "profit_margin" not in columns:
            print("Adding profit_margin column to estimates...")
            cursor.execute("ALTER TABLE estimates ADD COLUMN profit_margin FLOAT DEFAULT 0.0")
            conn.commit()
            
        print("Migration check complete.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
