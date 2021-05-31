from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

def get_menuno():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    menuno = int(input())
    print()
    return menuno

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def write_db(session, task, deadline):
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()

def query_db(session):
    return session.query(Table).all()

def show_task(session):
    rows = query_db(session)
    print("Today:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:    
        for row in rows:
            print(f"{row.id}. {row.task}")
    print()

def add_task(session):
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline = input()
    year, month, day = deadline.split("-")
    deadline = datetime(int(year), int(month), int(day))
    write_db(session, task, deadline)
    print("The task has been added!")
    print()

def show_today_tasks(session):
    today = datetime.today()
    day = today.strftime('%#d') 
    month = today.strftime('%b') 
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"Today: {day} {month}")
    if len(rows) == 0:
        print("Nothing to do!")
    else:    
        for i, row in enumerate(rows):
            print(f"{i + 1}. {row.task}")
    print()

def show_week_tasks(session):
    today = datetime.today()
    for i in range(7):
        weekday = today + timedelta(days=i)
        day = weekday.strftime('%#d') 
        month = weekday.strftime('%b')
        name_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dayofweek = name_list[weekday.weekday()]
        print(f"{dayofweek} {day} {month}.")
        rows = session.query(Table).filter(Table.deadline == weekday.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:    
            for i, row in enumerate(rows):
                print(f"{i + 1}. {row.task}")
        print()

def show_all_tasks(session):
    rows = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for i, row in enumerate(rows):
        day = row.deadline.strftime('%#d') 
        month = row.deadline.strftime('%b') 
        print(f"{i + 1}. {row.task}. {day} {month}")
    print()

def show_missed_task(session):
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    print(f"Missed Task:")
    if len(rows) == 0:
        print("Nothing is missed!")
    else:    
        for i, row in enumerate(rows):
            day = row.deadline.strftime('%#d') 
            month = row.deadline.strftime('%b') 
            print(f"{i + 1}. {row.task}. {day} {month}")
    print()

def delete_task(session):
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to do!")
        print()
        return    
    print("Choose the number of the task you want to delete:")
    idlist = []
    for i, row in enumerate(rows):
        day = row.deadline.strftime('%#d') 
        month = row.deadline.strftime('%b') 
        print(f"{i + 1}. {row.task}. {day} {month}")
        idlist.append(row.id)
    number = int(input())
    session.query(Table).filter(Table.id == idlist[number - 1]).delete()
    session.commit()
    print("The task has been deleted!")
    print()

while True:
    menuno = get_menuno()
    if menuno == 1:
        show_today_tasks(session)
    elif menuno == 2:
        show_week_tasks(session)
    elif menuno == 3:
        show_all_tasks(session)
    elif menuno == 4:
        show_missed_task(session)
    elif menuno == 5:
        add_task(session)
    elif menuno == 6:
        delete_task(session)
    elif menuno == 0:
        break

session.close()
print("Bye!")
