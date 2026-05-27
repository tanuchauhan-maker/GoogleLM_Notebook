from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.models.user import User
from app.models.notebook import Notebook
from app.models.chat_session import ChatSession
from app.models.message import Message

from app.schemas.chat import (
    MessageCreate,
    MessageResponse
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post(
    "/session/{session_id}",
    response_model=MessageResponse
)
def create_message(
    session_id: int,
    request: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session = db.query(ChatSession).join(Notebook).filter(
        ChatSession.id == session_id,
        Notebook.user_id == current_user.id
    ).first()

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    message = Message(
        session_id=session_id,
        role="user",
        content=request.content
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


@router.get(
    "/session/{session_id}",
    response_model=list[MessageResponse]
)
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session = db.query(ChatSession).join(Notebook).filter(
        ChatSession.id == session_id,
        Notebook.user_id == current_user.id
    ).first()

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).all()

    return messages