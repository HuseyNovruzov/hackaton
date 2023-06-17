from fastapi import APIRouter,status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from bson import ObjectId


from database import Report, User
from serializers.reportSerializer import reportEntity, reportResponseEntity
from serializers.usersSerializer import userEntity
import schemas
from . import oauth2

router = APIRouter()



@router.get('/reports', status_code=status.HTTP_200_OK)
async def get_reports(Authorize: AuthJWT = Depends(),user_id: str = Depends(oauth2.require_user)):
    try:
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='You are not allowed')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        print(user)

        return {"succes": "uploaded successfully"}
    except Exception:
        print(Exception) 