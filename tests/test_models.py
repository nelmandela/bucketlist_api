# import json
# import unittest
# from tests.base import Base
# from app.models import User
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine

# engine = create_engine('sqlite:///test_db', echo=True)
# Base = declarative_base()

# Session = sessionmaker(bind=engine)
# session = Session()

# class TestUserModel(Base):
#     def test_encode_auth_token(self):
#         user = User(
#         name='test',
#         email='test@test.com',
#         password='password'
#         )
#         session.add(user)
#         session.commit()
#         auth_token = user.encode_auth_token(user.id)
#         self.assertTrue(isinstance(auth_token, bytes))
#         self.assertEqual(response.status_code, 201)




# if __name__ == "__main__":
#     unittest.main()