from fastapi import APIRouter,status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from bson import ObjectId


from database import Report, User
from serializers.reportSerializer import reportEntity, reportResponseEntity
from serializers.usersSerializer import userEntity
import schemas
from . import oauth2

router = APIRouter()

@router.post('/send_report', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.ReportBaseSchema, Authorize: AuthJWT = Depends(),user_id: str = Depends(oauth2.require_user)):
    try:
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='You are not allowed')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        payload.user_id=ObjectId(str(user_id))
        result = Report.insert_one(payload.dict())
        return {"succes": "uploaded successfully"}
    except Exception:
        print(Exception)






