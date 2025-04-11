import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
import string

@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def set_roles(game_id):
  roles = ['pov', 'ineq', 'fut']
  regs = ['xy']
  ro_nbr = [0,1,2]
  for re in regs:
    for ro_n in ro_nbr:
      app_tables.roles_taken.add_row(game_id=game_id, reg=re, role_nbr = ro_n, role=roles[ro_n], taken=0)
  
@anvil.server.callable
def generate_id():
  cid = ''.join(random.choices(string.ascii_uppercase, k=3))
  a = random.randint(10, 99)
  cid = cid + '-' + str(a) 
  while app_tables.status.has_row(q.like(cid)):
    cid = ''.join(random.choices(string.ascii_uppercase, k=4))
    a = random.randint(10, 99)
    d = random.randint(10, 99)
    cid = cid + '-' + str(d) + '-' + str(a) 
  return f"{cid}"
  
