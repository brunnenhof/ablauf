from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import my_globs


class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_start_click(self, **event_args):
    game_id = anvil.server.call('generate_id')
    # for all regs being played !!!
    app_tables.status.add_row(game_id=game_id,closed=0,current_gm=0,current_p=0,reg='nix',pov=0,ineq=0,fut=0)
    pass

  def btn_join_click(self, **event_args):
    #no_game = app_tables.status.has_row()
    how_many_new = len(app_tables.status.search(closed=0, current_gm =0))
    if how_many_new > 1:
      self.card_top.visible = False
      self.card_select_game_to_join.visible = True
      self.select_game.items = [(row["game_id"], row) for row in app_tables.status.search(closed=0, current_gm =0, reg='nix')]
    elif how_many_new == 1:
      row = app_tables.status.get(closed=0)
      alert(row['game_id'], title="You are joining: ")
      my_globs.my_game_id = row['game_id']
      self.card_select_reg_role.visible = True
    else:
      alert("The game organizer has not yet started a game. Please wait until he/she does ...")
    pass

  def btn_join_after_selection_click(self, **event_args):
    alert(self.select_game.selected_value['game_id'], title="You are joining: ")
    game_id_chosen = self.select_game.selected_value['game_id']
    my_globs.my_game_id = game_id_chosen
#    alert(my_globs.my_game_id,"stored globally")
    self.card_select_game_to_join.visible = False
    self.card_select_reg_role.visible = True

  def get_role(self, **event_args):
    if self.rb_fut.selected: return 2
    if self.rb_pov.selected: return 0
    if self.rb_ineq.selected: return 1
      
  def btn_reg_role_chosen_click(self, **event_args):
    """Update status and my_globs"""
    which_reg = 'xy'
    which_role = self.get_role()
    row = app_tables.status.get(game_id=my_globs.my_game_id)
    app_tables.status.
    pass
