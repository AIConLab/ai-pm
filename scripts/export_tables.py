from mc_database import Database

if __name__ == ("__main__"):
    db = Database(db_path="/app/database/aipm.db")
    db.export_all_tables_to_json(output_dir="/app/database/")