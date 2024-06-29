
from vos import *

class MyApp(NodeApp):
    def __init__(self, vos, instancer=True):
        super().__init__(vos, "Alert", res=(600, 75))
        self.desktop = False
        self.text = "Hello world!"

    def run(self, text=None):
        app = super().run()
        if text: app.text = text
        app.text_node.text = app.text
        app.render_nodes()
        
    def on_run(self):
        super().on_run()
        self.setup_nodes()
        self.render_nodes()

    def on_confirm(self):
        self.close()

    def setup_nodes(self):
        w, h = self.res
        h //= 2

        self.children = []

        self.font = self.vos.load_font(size=20)
        
        self.text_node = TextNode(self, size=(w, h), pos=(0,0),
                                  text = self.text,
                                  font = self.font, center=True)
        
        self.confirm_node = ButtonNode(self, size=(w, h),
                                       pos=(0,h),
                                       text="OK", center=True,
                                       font = self.font,
                                       on_press=self.on_confirm)
        
        self.add(self.text_node)
        self.add(self.confirm_node)
