import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
import string
from . import my_globs
import pandas as pd

@anvil.server.callable
def upload_csv_data(dicts, rows=None):
  if rows:
    dicts = list(dicts)[:rows]
  for d in dicts:
    # d is now a dict of {columnname -> value} for this row
    # We use Python's **kwargs syntax to pass the whole dict as
    # keyword arguments
    app_tables.regions.add_row(**d)

@anvil.server.callable
def set_roles(game_id):
  roles = my_globs.roles
  regs = my_globs.regs
  ro_nbr = my_globs.ro_nbr
  re_nbr = my_globs.re_nbr
  npbp = my_globs.not_played_by_players
  for re in regs:
    if re in npbp:
      for ro_n in ro_nbr:
        app_tables.roles_taken.add_row(game_id=game_id, reg=re, role_nbr = ro_n, role=roles[ro_n], taken=2)  # 2 means role is filled by app
    else:
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
  
