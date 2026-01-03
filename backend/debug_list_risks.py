from sqlalchemy import create_engine, text
from app.core.config import settings

def debug_list_risks():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        print("--- Risk Events in riske schema ---")
        result = conn.execute(text("SELECT id, report_title, status, date, time FROM riske.risk_events ORDER BY created_at DESC"))
        rows = result.fetchall()
        if not rows:
            print("No risk events found.")
        for row in rows:
            print(row)

        print("\n--- Risk Approvals in riske schema ---")
        result = conn.execute(text("SELECT id, action, status, target_incident_id FROM riske.risk_approvals ORDER BY timestamp DESC"))
        rows = result.fetchall()
        for row in rows:
            print(row)

if __name__ == "__main__":
    debug_list_risks()
