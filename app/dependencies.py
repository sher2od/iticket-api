from app.db.session import LocalSession

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()