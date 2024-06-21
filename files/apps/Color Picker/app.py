from vos import *

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "Color Picker", (255 + 100, 100))

    def on_run(self):
        super().on_run()
        self.setup_nodes()

    def setup_nodes(self):
        self.children = []

        W, H = self.res

        slw, slh = W - H, H//4

        y = 0
        
        FG_CHANNEL = {
            'r':(255, 0, 0),
            'g':(0, 255, 0),
            'b':(0, 0, 255),
            'a':(255, 255, 255)
            }

        self.sliders = []
        for channel in 'rgba':
            slider = SliderNode(self, (0,y), (slw, slh+1), 255 if channel=='a' else 0, 255, rounded=True, fg=FG_CHANNEL[channel])
            self.sliders.append(slider)
            self.add(slider)
            y += slh

        self.view = RectNode(self, (slw, 0), (H, H))
        self.view.color = (0,0,0)
        self.add(self.view)

    def update(self):
        color = tuple([slider.value for slider in self.sliders])
        self.color = color
        color = [round(c*color[-1]/255) for c in color]
        self.view.color = color
        super().update()

    def render(self):
        self.render_nodes()
        super().render()
