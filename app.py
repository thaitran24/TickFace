from database import Database
from tkinter import Tk
from api import Slack
from gui import MainScreen
from gui import RecognitionScreen
from gui import IdentityScreen
from gui import CheckinScreen
from gui import RealnameScreen
from gui import ResetScreen
from gui import MainCanvas
from pathlib import Path
from utils import Time

class App():
    def __init__(self):
        self.init_layout()
        self.database = Database()

    def init_layout(self):
        self.window = Tk()
        self.window.title('TickFace')
        self.window.geometry('1024x720')
        self.window.configure(bg='#00EFFF')
        self.window.resizable(False, False)

        self.canvas = MainCanvas()
        self.canvas.place(x=0, y=0)

        self.main_screen = MainScreen(self.canvas, self.window)
        self.main_screen.set_start_btn_trans(self.main_screen_to_recog_screen)

        self.id_screen = IdentityScreen(self.canvas, self.window)
        self.id_screen.set_yes_btn_trans(self.id_screen_to_check_screen)
        self.id_screen.set_no_btn_trans(self.id_screen_to_rn_screen)

        self.checkin_screen = CheckinScreen(self.canvas, self.window)
        self.checkin_screen.set_checkin_btn_trans(self.confirm_checkin)
        self.checkin_screen.set_checkout_btn_trans(self.confirm_checkout)
    
        self.realname_screen = RealnameScreen(self.canvas, self.window)
        self.realname_screen.set_entry_btn_trans(self.rn_screen_to_check_screen)

        self.reset_screen = ResetScreen(self.canvas)

    def run(self):
        self.to_main_screen()
        self.window.mainloop()
    
    def to_main_screen(self):
        self.main_screen.enable()
    
    def to_reset_screen(self):
        self.reset_screen.enable()
        self.save_log()
        self.window.after(3000, self.reset_screen_to_main_screen)

    def to_recog_screen(self):
        self.recog_screen = RecognitionScreen(self.window)
        self.recog_screen.start_recognition()
        self.recog_info, self.img_frame = self.recog_screen.get_recog_info()
        self.recog_screen_to_id_screen()
    
    def to_id_screen(self):
        self.id_screen.enable()
        self.recog_info['name'] = Database().load_name(self.recog_info['id'])
        text = "Are you {} ?".format(self.recog_info['name'])
        self.id_screen.set_text(text=text)
        img_path = Path("./clipboard/result.png")
        self.id_screen.set_image(img_path)
        self.realname_screen.set_image(img_path)
        self.checkin_screen.set_image(img_path)

    def main_screen_to_recog_screen(self):
        self.main_screen.disable()
        self.window.after(500, self.to_recog_screen)

    def recog_screen_to_id_screen(self):
        self.main_screen.disable()
        self.to_id_screen()
    
    def id_screen_to_check_screen(self):
        self.id_screen.disable()
        self.recog_info['realname'] = self.recog_info['name']
        self.recog_info['true'] = True
        self.checkin_screen.enable()

    def id_screen_to_rn_screen(self):
        self.id_screen.disable()
        self.recog_info['true'] = False
        self.realname_screen.enable()
    
    def rn_screen_to_check_screen(self, *args):
        realname = self.realname_screen.get_entry()
        self.recog_info['realname'] = realname
        self.realname_screen.disable()
        self.checkin_screen.enable()
    
    def check_screen_to_reset_screen(self):
        self.checkin_screen.disable()
        self.window.after(500, self.to_reset_screen)
    
    def reset_screen_to_main_screen(self):
        self.reset_screen.disable()
        self.to_main_screen()
    
    def confirm_checkin(self):
        self.recog_info['check'] = 'check-in'
        self.check_screen_to_reset_screen()
    
    def confirm_checkout(self):
        self.recog_info['check'] = 'check-out'
        self.check_screen_to_reset_screen()

    def save_log(self):
        self.database.write_log(self.recog_info, self.img_frame)
        message = "{name} {check} at {time}".format(name=self.recog_info['realname'], 
                                                    check=self.recog_info['check'], 
                                                    time=Time().time(self.recog_info['time']))
        Slack.post(message=message)

if __name__=='__main__':
    app = App()
    app.run()
   