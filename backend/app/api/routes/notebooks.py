from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.models.notebook import Notebook
from app.models.user import User

from app.schemas.notebook import (
    NotebookCreate,
    NotebookResponse
)

router = APIRouter(
    prefix="/notebooks",
    tags=["Notebooks"]
)


@router.post(
    "/",
    response_model=NotebookResponse
)
def create_notebook(
    request: NotebookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notebook = Notebook(
        title=request.title,
        description=request.description,
        user_id=current_user.id
    )

    db.add(notebook)

    db.commit()

    db.refresh(notebook)

    return notebook


@router.get(
    "/",
    response_model=list[NotebookResponse]
)
def get_user_notebooks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notebooks = db.query(Notebook).filter(
        Notebook.user_id == current_user.id
    ).all()

    return notebooks