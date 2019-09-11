import os

import tornado.ioloop
import tornado.web
import tornado.options
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://qmx:123@localhost:3306/wensday')
Base = declarative_base(bind=engine)  # 这是一个基础类
Session = sessionmaker(bind=engine)  # 这是一个会话类

attr_dict = {'id': 'id', 'name': 'name', 'sex': 'sex', 'city': 'city', 'description': 'description',
             'birthday': 'birthday', 'only_child': 'only_child'}
# (id=id,name=name,sex=sex,city=city,description=desc,birthday=datetime.date(year,month,day),only_child=child)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    sex = Column(String(10), nullable=False)
    city = Column(String(10), default='北京', nullable=False)
    description = Column(String)
    birthday = Column(Date, default=datetime.date(1995, 1, 1))
    only_child = Column(Integer)


def get_session():
    session = Session()
    sql = session.query(Student)
    return session, sql


def query_by_id(id):
    session, sql = get_session()
    res = sql.get(str(id))
    session.commit()
    # print(res.id,res.name)
    return res


def get_all():
    session, sql = get_session()
    res = sql.filter().all()
    session.commit()
    return res





class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = self.get_argument('title', '我只是一张主页')
        sex = self.get_argument('sex', 'secret')

        # menu = ['蒸砖头', '烙窨井盖', '炒石头子', '红烧桌腿']
        self.render('index.html',
                    title=title,
                    sex=sex,

                    )


class SelectHandler(tornado.web.RequestHandler):
    def get(self):
        obj = get_all()
        count = len(obj)
        counts = range(1, count + 1)

        self.render('result.html', counts=counts)


class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        obj = get_all()
        count = len(obj)
        counts = range(1, count + 1)
        id = self.get_argument('id')
        name = obj[int(id) - 1].name
        sex = obj[int(id) - 1].sex
        city = obj[int(id) - 1].city
        desc = obj[int(id) - 1].description
        birth = obj[int(id) - 1].birthday
        child = obj[int(id) - 1].only_child

        self.render('show.html', id=id,
                    name=name,
                    sex=sex,
                    city=city,
                    desc=desc,
                    birth=birth,
                    child=child,
                    counts=counts)


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('update.html')

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        sex = self.get_argument('sex')
        city = self.get_argument('city')
        desc = self.get_argument('desc')
        year = self.get_argument('birthyear')
        month = self.get_argument('birthmonth')
        day = self.get_argument('birthday')
        child = self.get_argument('child')

        session, sql = get_session()
        get_result = sql.get(id)
        if get_result:
            try:
                get_result.name = name
                get_result.sex = sex
                get_result.city = city
                get_result.descritption = desc
                get_result.birthday = datetime.date(int(year), int(month), int(day))
                get_result.only_child = child
                session.commit()
                self.write('修改完成')
            except:
                self.write('修改失败')
        else:
            try:
                new = Student(id=id, name=name, sex=sex, city=city, description=desc,
                              birthday=datetime.date(int(year), int(month), int(day)), only_child=child)
                session.add(new)
                session.commit()
                self.write('添加完成')
            except:
                self.write('操作失败，请重试')


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        html = ('<form action="/delete" method="post">'
                '请输入需要查询的id:<input type="text" name="sid" value="">'
                '<br/>'
                '<input type="submit">'
                '</form>')
        self.write(html)

    def post(self):
        id = self.get_argument('sid')
        session, sql = get_session()
        try:
            old = sql.get(id)
            session.delete(old)
            session.commit()
            self.write('删除成功')
        except:
            self.write('删除失败,请输入正确的ID信息！！！')


routes = [
    (r"/query", SelectHandler),
    (r"/", MainHandler),
    (r"/show/", ShowHandler),
    (r"/update", UpdateHandler),
    (r"/delete", DeleteHandler)
]

file_path = os.path.dirname(__file__)
temp_path = os.path.join(file_path, 'temp')
static_path = os.path.join(file_path, 'static')


def make_app():
    return tornado.web.Application(routes, templates_path=temp_path, static_path=static_path)


def main():
    # get_all()
    app = make_app()
    app.listen(8000)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()

    # Base.metadata.create_all()
    # bob = Student(name='Bob', city='上海', birthday=datetime.date(1996, 1, 1), money=200)
    # tom = Student(name='Tom', city='US', birthday=datetime.date(1990, 1, 1), money=2)
    # jerry = Student(name='Jerry', city='US', birthday=datetime.date(1990, 1, 1), money=20)
    # bob.city='重庆'
    # session.add(bob)
    # session.add(tom)
    # session.add(jerry)
    # session.delete()#删除数据
    # session.add_all(list(listname)) # listname = [tom,bob,jerry]


if __name__ == "__main__":
    main()
