from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, create_db_engine, create_session_local

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def create_app(database_url: str = "sqlite:///./todo.db") -> FastAPI:
    engine = create_db_engine(database_url)
    session_local = create_session_local(engine)
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Markdoor Todo App", version="1.0.0")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    def get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/tasks", response_model=list[schemas.TaskResponse])
    def read_tasks(
        completed: Optional[bool] = Query(default=None),
        db: Session = Depends(get_db),
    ):
        return crud.list_tasks(db, completed=completed)

    @app.post("/api/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
    def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
        if not task_in.title.strip():
            raise HTTPException(status_code=400, detail="タスクタイトルは必須です")
        return crud.create_task(db, task_in)

    @app.put("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
    def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
        task = crud.get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")
        if task_in.title is not None and not task_in.title.strip():
            raise HTTPException(status_code=400, detail="タスクタイトルは空にできません")
        return crud.update_task(db, task, task_in)

    @app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int, db: Session = Depends(get_db)):
        task = crud.get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")
        crud.delete_task(db, task)
        return None

    return app


app = create_app()
