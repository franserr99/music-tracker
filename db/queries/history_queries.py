import datetime
from db.base import ScopedSession
from db.models.history import History
from db.queries.consts import SHORT,MEDIUM,LONG,TERM_TO_DAYS
#this assumes all songs passed to it are not in the db already


@staticmethod
def push_history_data(records:tuple, term:str, id:str):
    assert(term== SHORT or term==MEDIUM or term==LONG)
    #recall: the history table has the following fields: user_id, date_recorded, relative_term, track_id
    track_idx= records[0] 
    assert(len(track_idx)==len(records[1])==len(records[2]))
    #the timestamp used for all the records we are going to push right now 
    now= datetime.datetime.now() 
    session=ScopedSession()
    try:
        days_ago = now - datetime.timedelta(TERM_TO_DAYS[term])
        history = session.query(History).filter(History.user_id == id, History.relative_term == term).all()
        for record in history:
            #already recorded for this term within the relative time frame
            #check consts.py to see the translation
            if record.date_recorded > days_ago:
                print(f"{term} recorded within the last {TERM_TO_DAYS[term]/30} months already happened")
                return
        for track_ID  in track_idx :
            session.add(History(user_id=id, date_recorded= now, relative_term=term, track_id= track_ID))
        session.commit()    
    finally:
        session.close()   
@staticmethod
def get_listening_history( music_id:str): 
    session = ScopedSession()
    try:
        history=session.query(History).filter(History.user_id==music_id).all()
        return history
    finally:
        session.close()
@staticmethod
def get_listening_history_by_term(user_id:str, term:str): 
    assert(term==(SHORT or MEDIUM or LONG ))
    session = ScopedSession()
    #make model that represents the table
    try:
        history=session.query(History).filter(History.user_id==user_id, History.relative_term == term).all()
        return history
    finally:
        session.close()
@staticmethod
def get_most_recent_history(): 
    pass
@staticmethod
def get_songs_heard():
    pass