import uuid
from datetime import datetime

from src.admin.enums import AdminRoleEnum
from src.admin.schemas import Admin


async def authenticate_admin_override() -> Admin:
    return Admin(
        guid=uuid.uuid4(),
        email="admin@email.com",
        roles=[AdminRoleEnum.super_admin],
        hashed_password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
