# -*- conding:utf-8 -*-
import sqlite3


def start_num(uid, tag):

	conn = sqlite3.connect('mp-weixin.db')

	cursor = conn.cursor()

	cursor.execute('select * from message where uid=? AND sub=? ', (uid, tag,))

	start_num = 0
	for row in cursor:
		start_num = row[2]

	new_num = start_num + 1
	if start_num == 0:
		cursor.execute('insert into message values (?, ?, ?)', (uid, tag, new_num,))
	else:
		cursor.execute('update message set start=? where uid=? AND sub=?', (new_num, uid, tag,))
	conn.commit()
	cursor.close()
	conn.close()
	print(start_num)
	return start_num

if __name__ == '__main__':
	uid = "123"
	tag = "同性"
	start_num(uid,  tag)

