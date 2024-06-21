
from vos import *

class MyApp(NodeApp):
    def __init__(self, vos, instancer=True):
        super().__init__(vos, "Prompt", res=(350, 75))
        self.desktop = False
        self.callback = lambda x:self.vos.log("No callback for prompt. Response:",x)
        self.prompt = "Enter text:"

    def run(self, callback, prompt):
        app = super().run()
        app.callback = callback
        app.prompt = prompt

    def on_run(self):
        super().on_run()
        self.resp = ""
        self.vos.input.text = ""
        self.setup_nodes()
        self.render_nodes()
        self.focus()

    def on_confirm(self):
        self.callback(self.resp)
        self.close()

    def setup_nodes(self):
        w, h = self.res
        h //= 3

        self.children = []

        self.font = self.vos.load_font(size=20)
        self.prompt_node = TextNode(self, size=(w, h), pos=(0,0), text = self.prompt, font = self.font)
        self.resp_node = TextNode(self, size=(w, h), pos=(0,h), text = "...", font = self.font, center=False)
        self.confirm_node = ButtonNode(self, size=(w, h), pos=(0,h*2), text="CONFIRM",
                                       font = self.font, on_press=self.on_confirm)
        
        self.add(self.prompt_node)
        self.add(self.resp_node)
        self.add(self.confirm_node)

    def update(self):
        super().update()
        inp = self.vos.input
        if inp.text:
            self.resp += inp.text
            inp.text = ""
            self.resp_node.text = self.resp
            self.render_nodes()
        if pg.K_BACKSPACE in inp.keys:
            self.resp += self.resp[:-1]
            self.resp_node.text = self.resp
            self.render_nodes()

    def render(self):
        super().render()

        
