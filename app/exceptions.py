from fastapi import HTTPException

def handle_database_error():
    raise HTTPException(status_code=500, detail="Internal Server Error")

