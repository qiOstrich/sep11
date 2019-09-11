#!/bin/env python
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://qmx:123@localhost:3306/fornow')
Base = declarative_base(bind=engine)  # 这是一个基础类
Session = sessionmaker(bind=engine)  # 这是一个会话类


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20),unique=True,nullable=False)
    city = Column(String(10),default='北京')
    birthday = Column(Date, default=datetime.date(1970, 1, 1))
    money = Column(Float, default=0)

    # sex = Column()
    # only_child =Column()
    # description = Column()


def main():
    Base.metadata.create_all()
    c_SH ='上海'
    bob = Student(name='Bob', city=c_SH, birthday=datetime.date(1996, 1, 1),money=200)
    tom= Student(name='Tom', city='US', birthday=datetime.date(1990,1,1), money=2)
    jerry= Student(name='Jerry', city='US', birthday=datetime.date(1990,1,1), money=20)
    session = Session()
    # bob.city='重庆'
    session.add(bob)
    session.add(tom)
    session.add(jerry)


    # session.delete()#删除数据

    # session.add_all(list(listname)) # listname = [tom,bob,jerry]




    session.commit()

if __name__ == '__main__':
    main()
    # @you.setter
    # def you(self, y):
    #     self.you = y
    #
    # @property
    # def you(self):
    #     return self.you
