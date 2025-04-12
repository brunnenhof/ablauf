from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import webbrowser
from .. import my_globs


class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.title_top_left.text = my_globs.title_top_left_text
    self.rb_af.text = my_globs.regs[1]
    # Any code you write here will run before the form opens.

  def btn_start_click(self, **event_args):
    print('ok1')
    game_id = anvil.server.call('generate_id')
    # for all regs being played !!!
    print('ok')
    app_tables.status.add_row(game_id=game_id,closed=0,current_gm=0,current_p=0,reg='nix',roles_avail = 1)
    anvil.server.call('set_roles', game_id)
    alert("Roles set up")
    pass

  def show_regs(self, cid, reg):
    rows = app_tables.roles_taken.search(game_id=cid,reg=reg)
    for row in rows:
      if row['taken'] == 1:
        if row['role'] == 'pov':
          self.rb_pov.visible = False
        if row['role'] == 'ineq':
          self.rb_ineq.visible = False
        if row['role'] == 'fut':
          self.rb_fut.visible = False
    pass

  def show_roles(self, cid, reg):
    rows = app_tables.roles_taken.search(game_id=cid,reg=reg)
    for row in rows:
      if row['taken'] == 1:
        if row['role'] == 'pov':
          self.rb_pov.visible = False
        if row['role'] == 'ineq':
          self.rb_ineq.visible = False
        if row['role'] == 'fut':
          self.rb_fut.visible = False
    pass
    
  def btn_join_click(self, **event_args):
    #no_game = app_tables.status.has_row()
    print('btn_join')
    how_many_new = len(app_tables.status.search(closed=0, current_gm =0))
    if how_many_new > 1:
      self.card_top.visible = False
      self.card_select_game_to_join.visible = True
      self.select_game.items = [(row["game_id"], row) for row in app_tables.status.search(closed=0, current_gm =0, roles_avail=1)]
    elif how_many_new == 1:
      row = app_tables.status.get(closed=0)
      alert(row['game_id'], title="You are joining: ")
      my_globs.my_game_id = row['game_id']
      #### 
      #### xy must be replaced with the chosen region
      #### 
      self.show_roles(row['game_id'], 'xy')
      self.card_select_reg_role.visible = True
    else:
      alert("The game organizer has not yet started a game. Please wait until he/she does ...")
    pass

  def btn_join_after_selection_click(self, **event_args):
    alert(self.select_game.selected_value['game_id'], title="You are joining: ")
    game_id_chosen = self.select_game.selected_value['game_id']
    my_globs.my_game_id = game_id_chosen
    self.show_roles(game_id_chosen, 'xy')
#    alert(my_globs.my_game_id,"stored globally")
    self.card_select_game_to_join.visible = False
   
    self.card_select_reg_role.visible = True

  def get_role(self, **event_args):
    if self.rb_fut.selected: return 2
    if self.rb_pov.selected: return 0
    if self.rb_ineq.selected: return 1

  def all_roles_taken_for_region(self, cid, reg):
    rows = len(app_tables.roles_taken.search(game_id=cid, reg=reg, taken=0))
    if rows == 0:
      return True
    else:
      return False

  def all_roles_taken_for_game(self, cid, reg):
    for re in my_globs.regs:
      re_taken = self.all_roles_taken_for_region(self, cid, reg)
      if not re_taken:
        return False
    up = app_tables.status.get(game_id=cid)
    up.update(roles_avail=0)
    return True
    
  def btn_reg_role_chosen_click(self, **event_args):
    """Update status and my_globs"""
    which_reg = 'xy'
    which_role = self.get_role()
    row = app_tables.roles_taken.get(game_id=my_globs.my_game_id, reg=which_reg, role_nbr=which_role)
    row.update(taken = 1)
    self.all_roles_taken_for_game(my_globs.my_game_id, which_reg)
    ### make personal game_id, save in globals, display
    pass

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    #print(f"The file's name is: {file.name}")
    #print(f"The number of bytes in the file is: {file.length}")
    #print(f"The file's content type is: {file.content_type}")
#    print(f"The file's contents are: '{file.get_bytes()}'")
    b = file.get_bytes()
    bb = b.decode("utf-8")
    bbb = bb.splitlines()
    print(bbb)
    anvil.server.call('upload_csv_data', bbb, 'regs')

  def btn_thanks_click(self, **event_args):
    alert(content="... to our Alpha testers, the students in course SW101 at the Realschule Baesweiler during April 2024 taught by René Langohr, and all the beta testers.", title="Thank you", large=True)

  def btn_poc_click(self, **event_args):
    alert("Neither the user interface nor the server code is elegant nor efficient. Contact us if you can help making either or all better.",
         title="This app is a Proof of Concept")


  def btn_help_click(self, **event_args):
    webbrowser.open_new("http://sdggamehelp.blue-way.net")
