from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

import secrets
from pydantic import EmailStr

from . import oauth2
from database import User
from serializers.usersSerializer import userEntity, userResponseEntity
import schemas, utils
from config import settings
from input_verifier import isValidEmail, isValidPhoneNumber, isValidPassword
# from email_e import Email


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.CreateUserSchema):
    # Check if user already exist
    user = User.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    # Validate email
    if not isValidEmail(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email not a valid format!')
    # Validate phone number
    if not isValidPhoneNumber(payload.phone_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number does not math!")
    # Validate password 
    # if not isValidPassword(payload.password):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not match!")


    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')


    #  Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = 'user'
    payload.active = True
    payload.phone_number = f'+994{payload.phone_number}'
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = userResponseEntity(User.find_one({'_id': result.inserted_id}))

    # try:
    #     verification_code = secrets.token_hex(16)
        
    #     User.find_one_and_update({"_id": result.inserted_id}, {"$set": {"verification_code": verification_code, "updated_at": datetime.utcnow()}})

    #     url = f"http://localhost:3000/api/auth/verifyemail/{verification_code}"
    #     await Email(userEntity(new_user), url, [EmailStr(payload.email)]).sendVerificationCode()
    
    # except Exception as error:
    #     User.find_one_and_update({"_id": result.inserted_id}, {
    #         "$set": {"verification_code": None, "updated_at": datetime.utcnow()}})
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail='There was an error sending email')
    
    return {"status": "success", "user": new_user}


@router.post('/login')
def login(payload: schemas.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    # Check if the user exist
    db_user = User.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = userEntity(db_user)

    # Check if the password is valid
    if not utils.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token}


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}

