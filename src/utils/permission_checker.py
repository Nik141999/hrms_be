from fastapi import Depends, HTTPException, status
from src.utils.auth import get_current_user
from src.models.user import User
from src.models.organization import Organization

def PermissionChecker(route: str, action: str):
    async def checker(user_or_org: User | Organization = Depends(get_current_user)):
        role = getattr(user_or_org, "role", None)

        if not role or not role.permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role permissions not set."
            )

        for perm in role.permission:
            perm_route = perm.get("route", "")
            perm_actions = perm.get("permission", {})

            # Match exact or route prefix (e.g. /users matches /users/{user_id})
            if route == perm_route or route.startswith(perm_route + "/"):
                if perm_actions.get(action):
                    return  # ✅ Permission granted
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have permission to perform this action"
                    )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission rule defined for this route"
        )

    return checker
