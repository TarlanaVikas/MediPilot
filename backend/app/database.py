import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Healthcare Database
# ============================================================

DATABASE_FILE = DATA_DIR / "healthcare.db"

DATABASE_URL = (
    f"sqlite:///{DATABASE_FILE}"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


Base = declarative_base()


# ============================================================
# Initialization
# ============================================================

def _seed_default_doctors() -> None:
    """Seed the SQLite database with the bundled doctor catalog if empty."""

    from backend.app.doctor_import import import_doctors

    db = SessionLocal()
    try:
        from backend.app.models import Doctor

        if db.query(Doctor).count() > 0:
            return

        project_root = Path(__file__).resolve().parents[2]
        doctors_file = project_root / "data" / "doctors.json"

        if not doctors_file.exists():
            return

        doctors = json.loads(doctors_file.read_text(encoding="utf-8"))
        if not isinstance(doctors, list) or not doctors:
            return

        seeded = []
        for doctor in doctors:
            name = doctor.get("name", "").strip()
            if not name:
                continue

            seeded.append({
                "name": name,
                "specialty": doctor.get("specialty", "").strip(),
                "experience": int(doctor.get("experience", 0) or 0),
                "description": doctor.get("description", "") or "",
                "availability": [
                    {
                        "date": "2026-10-02",
                        "time_slots": ["09:00", "11:00"],
                    },
                    {
                        "date": "2026-10-03",
                        "time_slots": ["09:00", "10:00", "14:00"],
                    },
                    {
                        "date": "2026-10-04",
                        "time_slots": ["10:00", "15:00"],
                    },
                ],
            })

        if seeded:
            import_doctors(seeded)
    finally:
        db.close()


def init_db():
    """Create healthcare application tables and seed demo data if needed."""

    from backend.app.models import (
        Appointment,
        Doctor,
        DoctorAvailability,
        Patient,
    )

    Base.metadata.create_all(
        bind=engine,
    )
    _seed_default_doctors()


init_db()