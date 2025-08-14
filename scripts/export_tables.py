from mc_database import Database
from utils import load_config

if __name__ == ("__main__"):

    config = load_config()
    
    db = Database(
        db_path="/app/database/aipm.db",
        user_config=config
        )
    
    db.init_tables()

    db.export_all_tables_to_json(output_dir="/app/database/")