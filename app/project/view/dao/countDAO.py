import sqlite3 as sql

def create_cnt():
    try:
        conn = sql.connect("duck.db")
        cur = conn.cursor()
        s = """
            INSERT INTO counts(cal)
              VALUES(strftime('%Y-%m-%d', 'now'))
              ON CONFLICT(cal)
              DO UPDATE SET cnt = cnt + 1;
            """
        cur.execute(s)
        conn.commit()
        return True
    except Exception:
        return False  

def select_cnt():
    try:
      conn = sql.connect("duck.db")
      cur = conn.cursor()
      s = """
          SELECT * FROM counts 
            WHERE cal=strftime('%Y-%m-%d', 'now');
          """
      cur.execute(s)
      cnt = cur.fetchone()
      return cnt[1]
    except Exception:
      return False  