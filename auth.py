from fastapi import FastAPI, Header,HTTPException
from typing import Union
import jwt


class RoleAccess:
    user_role = ''
    def __init__(self,*role):
        self.role = role


    def __call__(self,token: Union[str,None]= Header(default=None)):
        if token==None:
            raise HTTPException(
                status_code=401,
                detail="You are not authorized as token is not included"
            )
    
        try:
            print(token)
            decoded_jwt = jwt.decode(token,options={"verify_signature": False})
            print(decoded_jwt)
            user_role = decoded_jwt['realm_access']['roles'][0]
        except:
            raise HTTPException(
                status_code=400,
                detail="We can't extract the informations since you didn't provid the correct token"

            )

        if user_role not in self.role:
            raise HTTPException(
                status_code=403,
                detail=f"Role : {user_role} is not allowed"
            )

admin = RoleAccess("admin")
user = RoleAccess("user","admin")