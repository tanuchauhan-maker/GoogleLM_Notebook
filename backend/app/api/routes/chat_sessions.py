from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.models.user import User
from app.models.notebook import Notebook
from app.models.chat_session import ChatSession

from app.schemas.chat import ChatSessionCreate, ChatSessionResponse

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/chat-sessions",
    tags=["Chat Sessions"]
)


@router.post(
    "/notebook/{notebook_id}",
    response_model=ChatSessionResponse
)
def create_chat_session(
    notebook_id: int,
    request: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notebook = db.query(Notebook).filter(
        Notebook.id == notebook_id,
        Notebook.user_id == current_user.id
    ).first()

    if not notebook:

        raise HTTPException(
            status_code=404,
            detail="Notebook not found"
        )

    session = ChatSession(
        notebook_id=notebook_id,
        title=request.title
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


@router.get(
    "/notebook/{notebook_id}",
    response_model=list[ChatSessionResponse]
)
def get_chat_sessions(
    notebook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notebook = db.query(Notebook).filter(
        Notebook.id == notebook_id,
        Notebook.user_id == current_user.id
    ).first()

    if not notebook:

        raise HTTPException(
            status_code=404,
            detail="Notebook not found"
        )

    sessions = db.query(ChatSession).filter(
        ChatSession.notebook_id == notebook_id
    ).all()

    return sessions