from app import app
from models import *

with app.app_context():

    #Delete tables first before populating to avoid duplication of data
    User.query.delete()
    JournalEntry.query.delete()

    #Populate users data
    users = [
        User(username='John Doe', password='jOhNdOE123'),
        User(username='Jane Doe', password='janeDOE@14'),
        User(username='Kevin Hart', password='kevin@hart123')
    ]

    db.session.add_all(users)
    db.session.commit()

    #Populate journal entries
    journal_entries = [
        JournalEntry(title='Learn Python With Me', content='Learn detailed Python topics', user_id=1),
        JournalEntry(title='How to Learn to Program', content='Understand how to create systems and programs', user_id=2),
        JournalEntry(title='How to Play Poker', content='Understand the different divisions of Poker and how to play them', user_id=3),
        JournalEntry(title='How to make a perfect bet', content='Know how to call, fold or raise', user_id=4)
    ]
    
    db.session.add_all(journal_entries)
    db.session.commit()



