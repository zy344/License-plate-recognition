# n = 3
# names = ["Alice", "Bob", "Charlie"]
# print(f"{n} {names[1]}{'s' * (n > 1)}, ")

# import torch
#
# det = torch.tensor([[204.81831, 335.46518, 440.51141, 396.68887,   0.91313,   0.00000],
#         [-12.12469, -13.56367, 642.46509, 437.59851,   0.88991,   1.00000]], device='cuda:0')
# print(det[:, :4])

# print({} and 1)
# print(1 and 0)
# print(0 and 0)
# print(False and False)
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="Car_wash_room"
)
"""
cursor = db.cursor()
sql = "INSERT INTO use_data (id, name, phone, plate) VALUES (%s, %s, %s, %s)"

names = ['小张', '小白', '小爱']
phones = ['332111', '1122334', '11334']
plates = ['京QF60F0', '京C77777', '皖AD08815']
for i in range(3):
    values = (i+1, names[i], phones[i], plates[i])
    print(values)
    cursor.execute(sql, values)

# 提交更改到数据库
db.commit()

print(f"插入了 {cursor.rowcount} 条记录")
"""


cursor = db.cursor()
sql = "select exists (select 1 from use_data where plate = '京QF60F0') As is_exists"
cursor.execute(sql)
print(bool(cursor.fetchone()[0]))