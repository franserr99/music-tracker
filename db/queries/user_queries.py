from db.base import ScopedSession
from db.models.user import User

def create_user(id: str ):
    print("user being created")
    try:
        session=ScopedSession()
        new_user=User(id=id)
        session.add(new_user)
        session.commit() 
    finally:
        session.close()
        pass
def users_list():    
    try:
        session=ScopedSession()
        user_list= session.query(User).all()  
        return user_list
    finally:
        pass
        session.close()
def user_id_list():
    users=users_list()
    IDs=[]
    for user in users:
        IDs.append(user.id)
    return IDs