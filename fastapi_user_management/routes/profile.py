"""User endpoint ``/user``."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.core.database import get_db
from fastapi_user_management.models.user import UserModel
from fastapi_user_management.routes import auth
from fastapi_user_management.schemas.user import UserBase

router = APIRouter(
    prefix="/user",
    tags=["profile"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    },
)


@router.get("", response_model=UserBase)
async def read_user_profile(
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
    username: str = "",
    id: int = 0,
):
    """Read a user's profile by username or ID.

    Args:
        current_user (Annotated[UserModel, Depends): The currently logged-in user.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        username (str, optional): The username to search for. Defaults to an empty string.
        id (int, optional): The user ID to search for. Defaults to 0.

    Raises:
        HTTPException: Raises a 404 status code if the user is not found.
        HTTPException: Raises a 500 status code for any unexpected server errors.

    Returns:
        UserBase: The user profile that matches the provided username or ID.
    """
    try:
        user = None
        if id > 0:
            user = crud.user.get_by_id(db=db, id=id)
        elif username != "":
            user = crud.user.get_by_username(db=db, username=username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
