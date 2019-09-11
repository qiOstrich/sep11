import tornado.ioloop
import tornado.web
import pymysql

update_dict = {}
select_dict = {}

db = None
# def insert_values(cur,dict):
#     sql_insert = '''insert into wensday.student set name ='{name}', sex ='{sex}', city='{city}', description='{desc}', birthday ='{birthyear}-{birthmonth}-{birthday}', only_child ={child}, id ={id};'''
#     cur.execute(sql_insert.format(**dict))

def connetdb():
    global db
    db = pymysql.connect(
        host='localhost',
        user='qmx',
        password='123',
        database='wensday',
        charset='utf8'
    )
    cur = db.cursor()

    return cur


def close():
    global db
    db.commit()
    db.close()


def select_by_id(cur, dict):
    sql_select = 'select * from wensday.student where id = {id};'
    cur.execute(sql_select.format(**dict))
    result = cur.fetchall()
    # print('当前的数据：', result)
    return result


def update(cur, dict):
    sql_update = '''update wensday.student set name ='{name}', sex ='{sex}', city='{city}', description='{desc}', birthday ='{birthyear}-{birthmonth}-{birthday}', only_child ={child} where id ={id};'''
    cur.execute(sql_update.format(**dict))


# def select_all(cur):
#     sql_select_all = 'select * from wensday.student;'
#     cur.execute(sql_select_all)
#     return cur.fetchall()


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        html = ('<form action="/update" method="post">'
                'id:<input type="text" name="id" value=""><br/>'
                'name:<input type="text" name="name" value=""><br/>'
                'sex:<input type="radio" name="sex" value="男">男'
                '<input type="radio" name="sex" value="女">女<br/>'
                'city:<input type="text" name="city" value=""><br/>'
                '简介:<textarea name="desc"></textarea><br/>'
                'birth:<br/>'
                'year<input type="text" name="year">'
                'month<input type="text" name="month">'
                'day<input type="text" name="day"><br/>'
                '独生子:<input type="radio" name="child" value="1">是'
                '<input type="radio" name="child" value="0">否'
                '<br/>'
                '<input type="submit">'
                '<input type="reset" value="重置!!!慎点!!!">'
                '</form>')
        self.write(html)

    def post(self):
        global db
        def get_data():
            id = self.get_argument('id')
            update_dict['id'] = id
            name = self.get_argument('name')
            update_dict['name'] = name
            sex = self.get_argument('sex')
            update_dict['sex'] = sex
            city = self.get_argument('city')
            update_dict['city'] = city
            desc = self.get_argument('desc')
            update_dict['desc'] = desc
            birthyear = self.get_argument('year')
            update_dict['birthyear'] = birthyear
            birthmonth = self.get_argument('month')
            update_dict['birthmonth'] = birthmonth
            birthday = self.get_argument('day')
            update_dict['birthday'] = birthday
            only_child = self.get_argument('child')
            update_dict['child'] = only_child
        try:
            get_data()
        except:
            pass
        cur = connetdb()
        res = select_by_id(cur, update_dict)
        if res:
            update(cur, update_dict)
            select_by_id(cur, update_dict)
            self.write('修改数据成功')
        else:
            # insert_values(cur, update_dict)
            self.write('没有找到这个ID')
        close()


class SelectHandler(tornado.web.RequestHandler):
    def get(self):
        html = ('<form action="/select" method="post">'
                '请输入需要查询的id:<input type="text" name="sid" value="">'
                '<br/>'
                '<input type="submit">'
                '</form>')
        self.write(html)

    def post(self):
        global db

        def get_data():
            id = self.get_argument('sid')
            select_dict['id'] = id

        get_data()
        # print(select_dict)
        try:
            cur = connetdb()
            get = select_by_id(cur, select_dict)
            # print(get)
            if get:
                self.write('你查询的数据是：{}'.format(get))
            else:
                self.write('查询的ID不存在哦')
        except Exception as f:
            print(f)
            self.write('查询出错了')
        finally:
            try:
                close()
            except:
                pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = ('<a href="http://localhost:8880/select">通过ID查找</a><br/>'
                '<a href="http://localhost:8880/update">修改数据</a>')
        self.write(html)


def make_app():
    return tornado.web.Application(
        [(r"/update", UpdateHandler),
         (r"/select", SelectHandler),
         (r"/", MainHandler),
         ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8880)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
