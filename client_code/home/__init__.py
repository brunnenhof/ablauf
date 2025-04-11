from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_start_click(self, **event_args):
    game_id = anvil.server.call('generate_id')
    # for all regs being played !!!
    app_tables.status.add_row(game_id=game_id,closed=0,current_gm=0,current_p=0,reg='xy',pov=0,ineq=0,fut=0)
    pass

  def btn_join_click(self, **event_args):
    #no_game = app_tables.status.has_row()
    how_many_open = len(app_tables.status.search(closed=0))
    how_many_new = len(app_tables.status.search(closed=0, current_gm =0))
    alert(how_many,title="How many open games")
    Notification(how_many_new,'How many newly started')
    if how_many_open > 1:
      
    one_game
    """This method is called when the button is clicked"""
    pass
