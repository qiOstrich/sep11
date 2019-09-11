import tornado.ioloop
import tornado.web
import pymysql

update_dict = {}
select_dict = {}

db = None


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


def insert_values(cur, dict):
    sql_insert = '''insert into wensday.student set name ='{name}', sex ='{sex}', city='{city}', description='{desc}', birthday ='{birthyear}-{birthmonth}-{birthday}', only_child ={child}, id ={id};'''
    cur.execute(sql_insert.format(**dict))


def delete_by_id():
    pass


def update(cur, dict):
    sql_update = '''update wensday.student set name ='{name}', sex ='{sex}', city='{city}', description='{desc}', birthday ='{birthyear}-{birthmonth}-{birthday}', only_child ={child} where id ={id};'''
    cur.execute(sql_update.format(**dict))


def select_by_id(cur, dict):
    sql_select = 'select * from wensday.student where id = {id};'
    cur.execute(sql_select.format(**dict))
    result = cur.fetchall()
    # print('当前的数据：', result)
    return result


def select_all(cur):
    sql_select_all = 'select * from wensday.student;'
    cur.execute(sql_select_all)
    show_list=[]
    while 1 :
        result = cur.fetchone()
        if result:
            show_list.append(result)
        else:
            break
    return show_list


def close():
    global db
    db.commit()
    db.close()


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

        get_data()
        cur = connetdb()
        res = select_by_id(cur, update_dict)
        if res:
            try:
                update(cur, update_dict)
                select_by_id(cur, update_dict)
                self.write('修改数据成功')
            except:
                self.write('请正确输入信息!')
        else:
            try:
                insert_values(cur, update_dict)
                self.write('没有找到这个ID,将会为你插入这条数据')
            except:
                self.write('请正确输入信息!')

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
            print(get)
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
        html = ('<a href="http://localhost:8080/select">通过ID查找</a><br/>'
                '<a href="http://localhost:8080/update">修改数据</a>'
                '<a href="http://localhost/showall"></a>')
        self.write(html)
class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            cur = connetdb()
            select_all(cur)
        except:
            pass
        html = ''

def make_app():
    return tornado.web.Application(
        [(r"/update", UpdateHandler),
         (r"/select", SelectHandler),
         (r"/", MainHandler),
         (r"/showall", ShowHandler)
         ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
