
from fastapi import APIRouter, HTTPException
from pymysql.err import IntegrityError

from schemas.user import UserCreate
from crud.users import create_user_record, get_user_record


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=201)
def create_user(user: UserCreate):
    try:
        new_user = create_user_record(
            name=user.name,
            email=str(user.email)
        )

        return {
            "message": "User created successfully",
            "user": new_user
        }

    except IntegrityError as error:
        if error.args[0] == 1062:
            raise HTTPException(
                status_code=409,
                detail="This email already exists"
            )

        raise HTTPException(
            status_code=400,
            detail="Could not create user"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not create user"
        )


@router.get("/{user_id}")
def get_user(user_id: int):
    try:
        user = get_user_record(user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve user"
        )
