from vos import *

class MyApp(App):
    def __init__(self, vos):
        super().__init__(vos, "start")
        self.desktop = False
    def run(self):
        self.vos.get_app("Desktop").run()
        apps = self.vos.get_app("Settings").get("on-start")
        if apps:
            for app in eval(apps):
                print(app)
                self.vos.get_app(app).run()
