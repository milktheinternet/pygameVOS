from vos import *

class MyApp(App):
    def __init__(self, vos):
        super().__init__(vos, "Power Off")
    def run(self):
        self.vos.input.quit = True
