import pymysql
import time
import threading

class SQLcommand:
  conn = pymysql.connect(
    host = 'db',
    database = 'chi101',
    user = 'chi101',
    password = 'chi101',
    charset = 'utf8mb4'
  )

  def get(self, sql: str) -> tuple:
    while True:
      try:
         with self.conn.cursor() as cursor:
           cursor.execute(sql)
           data = cursor.fetchall()
         return data
      except pymysql.err.InterfaceError:
         time.sleep(2)
      except pymysql.err.OperationalError:
         time.sleep(2)    
  
  def modify(self, sql: str) -> None:
    with self.conn.cursor() as cursor:
      cursor.execute(sql)
    self.conn.commit()

  def modify_tuple(self, sql: str, values: tuple) -> None:
    with self.conn.cursor() as cursor:
      cursor.execute(sql, values)
    self.conn.commit()
    
  def keep_alive(self):
    with self.conn.cursor() as cursor:
        cursor.execute("SELECT 1")
    # 每隔1小時（3600秒）執行一次查詢
    threading.Timer(3600, self.keep_alive).start()

if __name__ == '__main__':
  pass
  
# Instantiate the SQLcommand class
sql_command = SQLcommand()

# Start a new thread that runs the keep_alive method in the background
threading.Thread(target=sql_command.keep_alive).start()  
