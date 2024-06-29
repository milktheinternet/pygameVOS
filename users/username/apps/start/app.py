from vos import *

class MyApp(App):
    def __init__(self, vos):
        super().__init__(vos, "start")
        self.desktop = False
    def run(self):
        self.vos.get_app("Desktop").run()
        for app in self.vos.get_app("Settings").get("on-start"):
            self.vos.get_app(app).run()
