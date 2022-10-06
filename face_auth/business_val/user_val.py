import sys
import os
import re
import uuid
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from dotenv import dotenv_values

# from face_auth.entity.user import Login, Register
from face_auth.entity.user import User
from face_auth.data_access.user_data import UserData
from face_auth.exception import AppException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        

class LoginValidation:
    """_summary_
    """
    def __init__(self, email_id: str, password: str):
        """_summary_

        Args:
            email_id (str): _description_
            password (str): _description_
        """
        self.email_id = email_id
        self.password = password
    
    def verifyPassword(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt_context.verify(plain_password, hashed_password)
    
    def authenticateUserLogin(self) -> Optional[str]:
        """_summary_: This authenticates the user and returns the token
        if the user is authenticated

        Args:
            email_id (str): _description_
            password (str): _description_
        """
        try:
            userdata = UserData()
            user_login_val = userdata.get_user({"email_id": self.email_id})
            if not user_login_val:
                return False
            if not self.verifyPassword(self.password, user_login_val['password']):
                return False
            return user_login_val
        except Exception as e:
            raise e
    








class RegisterValidation:


    def __init__(self, user: User) -> None:
        try:
            print("Inside RegisterValidation")
            self.user = user
            self.regex= re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            self.uuid = self.user.uuid_ 
            self.userdata = UserData()
            self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            print("Completed RegisterValidation")   
        except Exception as e:
            raise e

    def validate(self) -> bool:

        """This checks all the validation conditions for the user registration

        Returns:
            _type_: string
        """
        try:
            msg=""
            if self.user.Name == None:
                msg+="Name is required"

            if self.user.username == None:
                msg+="Username is required"

            if self.user.email_id == None:
                msg+="Email is required"

            if self.user.ph_no == None:
                msg+="Phone Number is required"

            if self.user.password1 == None:
                msg+="Password is required"

            if self.user.password2 == None:
                msg+="Confirm Password is required"

            if not self.isEmailValid():
                msg+="Email is not valid"

            if not self.isPasswordValid():
                msg+="Length of the pass`word should be between 8 and 16"

            if not self.isPasswordMatch():
                msg+="Password does not match"
                
            if not self.isDetailsExists():
                msg+="User already exists"

            print(msg)
            return msg
        except Exception as e:
            raise e
    
    def isEmailValid(self) -> bool:
        if re.fullmatch(self.regex, self.user.email_id):
            return True
        else:
            return False
    
    def isPasswordValid(self) -> bool:
        if len(self.user.password1) >= 8 and len(self.user.password2) <= 16:
            return True
        else:
            return False
    
    def isPasswordMatch(self) -> bool:
        if self.user.password1 == self.user.password2:
            return True
        else:
            return False
    
    def isDetailsExists(self) -> bool:
        username_val = self.userdata.get_user({"username": self.user.username})
        emailid_val = self.userdata.get_user({"email_id": self.user.email_id})
        uuid_val = self.userdata.get_user({"UUID": self.uuid})
        # print(username_val, emailid_val, uuid_val)
        if username_val == None and emailid_val == None and uuid_val == None:
            return True
        return False
    
    @staticmethod
    def getPasswordHash(password: str) -> str:
            return bcrypt_context.hash(password)

    

    def validateRegistration(self) -> bool:

        """This checks all the validation conditions for the user registration
        """
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def saveUser(self) -> bool:
        """_summary_: This saves the user details in the database
        only after validating the user details

        Returns:
            bool: _description_
        """
        if self.validateRegistration()['status']:
            hashed_password: str = self.getPasswordHash(self.user.password1)
            user_data_dict: dict= {"Name": self.user.Name, "username": self.user.username, "password": hashed_password,\
                     "email_id": self.user.email_id, "ph_no": self.user.ph_no, "UUID": self.uuid}
            self.userdata.save_user(user_data_dict)
            return {"status": True, "msg": "User registered successfully"}
        return {"status": False, "msg": self.validate()}