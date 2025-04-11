import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random

@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def generate_id(name):
    cid = ''.join(random.choices(string.ascii_uppercase, k=2))
    a = random.randint(10, 99)
    d = random.randint(10, 99)
    cid = cid + '-' + str(d) + '-' + str(a) 
    # cid = 'TEST'  #  while testing ...
    return f"{cid}"
  
  print("Hello, " + name + "!")
  return 42
