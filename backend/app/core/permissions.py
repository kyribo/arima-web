from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.api.v1.auth import get_current_user

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, user: User = Depends(get_current_user)):
        # Superadmin role bypass
        if user.role == "Superadmin":
            return user

        # Superadmin wildcard check
        if "*" in user.access:
            return user
            
        if self.required_permission not in user.access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have permission to access this resource. Required: {self.required_permission}"
            )
        return user
