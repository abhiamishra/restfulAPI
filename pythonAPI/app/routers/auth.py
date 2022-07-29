from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(database.get_db)):

        user = db.query(models.User).filter(models.User.email == user_cred.username).first()

        if user == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Invalid Credentials")
        
        if not utils.verifyIt(user_cred.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail = f"Invalid Credentials")
        
        #Creating JWT Token
        access_token = oauth2.create_access_token(data={
            "user_id": user.uid
        })

        print("USER.UID")
        print(user.uid)

        #Returning token

        return {"access_token" : access_token, "token_type": "bearer"}
