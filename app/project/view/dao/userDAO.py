import hashlib #sha256
import sqlite3 as sql
# from typing import final

class User():
  def __init__(self, email, pw=0, birth=0, sex=0):
    self.email = email
    self.pw = pw
    self.birth = birth
    self.sex = sex

  def __str__(self):
    return print(f"email:{self.email}, pw:{self.pw}, birth:{self.birth}, sex:{self.sex}")
    
  def to_dict(self):
    return {"email":self.email, "pw":self.pw, "birth":self.birth, "sex":self.sex}

  def create_user(self):
    if self.validation_user():  #signup validation
      return False
    else:
      try:
        self.pw = hashlib.sha256(self.pw.encode())
        self.pw = self.pw.hexdigest()
        conn = sql.connect("duck.db")       
        cur = conn.cursor()
        s = """
            INSERT INTO users(email, pw, birth, sex) 
                VALUES(:email, :pw, :birth, :sex)
            """
        # print(self.to_dict())
        cur.execute(s, self.to_dict())
        conn.commit()
      except Exception:
        conn.rollback()
        conn.close()
        return False
      finally:
        conn.close()
        return True

  #id 유효성 검사
  def validation_user(self):
    try:
      conn = sql.connect("duck.db")       
      cur = conn.cursor()
      s = """
          SELECT * FROM users 
          WHERE email=:email
          """
      cur.execute(s, {"email":self.email})
      data = cur.fetchone()

      if data and data[0] == self.email:
        raise Exception
      else:
        return False
    except Exception:
      conn.close()
      return True

  def login_user(self):
    try:
      self.pw = hashlib.sha256(self.pw.encode())
      self.pw = self.pw.hexdigest()
      conn = sql.connect("duck.db")
      cur = conn.cursor()

      s = """
          SELECT * FROM users
            WHERE email=:email and pw=:pw
          """
      cur.execute(s, {"email":self.email, "pw":self.pw})
      data = cur.fetchone()

      if data:
        user = User(*data)
        return True
      else:
        raise Exception
    except Exception:
      conn.close()
      return False