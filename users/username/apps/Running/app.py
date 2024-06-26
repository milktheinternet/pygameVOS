from vos import *

class MyApp(TextApp):
    def __init__(self, vos):
        super().__init__(vos, "Running", (300, 400), font=None)

    def idle_render(self):
        self.update_render("\n".join(reversed(
            [app.name for app in self.vos.running])))
        super().idle_render()
