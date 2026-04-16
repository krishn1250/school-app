from pathlib import Path
import sys

from fastapi.testclient import TestClient

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

if (PROJECT_DIR / "main.py").exists():
    from main import app
else:
    app_root = PROJECT_DIR / "school-crud"
    if str(app_root) not in sys.path:
        sys.path.insert(0, str(app_root))
    from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
