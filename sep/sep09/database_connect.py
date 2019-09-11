import pymysql

db = pymysql.connect(
    host='localhost',
    user='qmx',
    password='123',
    database='wensday',
    charset='utf8'

)
cur = db.cursor()
update_dict = {'name': '陈乔恩', 'sex': '女', 'city': '上海', 'desc': '是好看', 'birthyear': '1995', 'birthmonth': '03',
               'birthday': '02', 'child': '1'}
update_dict['id'] = 2
sql_select_all = 'select * from wensday.student;'
sql_select = 'select * from wensday.student where id = %s;'
sql_update = '''update student set name ='{name}', sex ='{sex}', city='{city}', description='{desc}', birthday ='{birthyear}-{birthmonth}-{birthday}', only_child ={child} where id ={id};'''
cur.execute(sql_update.format(**update_dict))

# fs= sql_update.format(**{'id':2,'name':'陈乔恩','sex':'女','city':'上海','desc':'是好看','birthyear':'1995','birthmonth':'03','birthday':'02','child':'1'})
# print (fs)
# update student set description = '这家伙很勤奋, 但还是什么都没留下。。。' where id =10;
cur.execute(sql_select, 10)
print(cur.fetchall())
db.close()
