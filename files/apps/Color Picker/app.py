from vos import *

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "Color Picker", (255 + 100, 100))
        self.callback = lambda color:self.vos.log("Color Picker returned",str(color))

    def on_run(self):
        super().on_run()
        self.setup_nodes()

    def set_color(self, color):
        self.color = color
        for i in range(len(color)):
            self.sliders[i].set_value(color[i])

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
            slider = SliderNode(self, (0,y), (slw, slh+1), 255 if channel=='a' else 0, 255, rounded=True,
                                fg=FG_CHANNEL[channel])
            text = TextNode(self, (0,y), (slw, slh+1), center=True, nobg=True)
            def create_change_function(slider, text_node):
                def func(val):
                    self.last_slider = slider
                    text_node.text = str(val)
                return func
            slider.on_change = create_change_function(slider, text)
            self.sliders.append(slider)
            self.last_slider = slider
            self.add(slider)
            self.add(text)
            y += slh
        for slider in self.sliders:
            slider.on_change(slider.value)

        cbw = cbh = 4
        cb1, cb2 = (100, 100, 100), (133, 133, 133)
        cbsrf = pg.Surface((cbw, cbh))
        cbsrf.fill(cb1)
        for x in range(cbw):
            for y in range(cbh):
                if x%2==y%2:
                    cbsrf.set_at((x,y), cb2)
        self.checkerboard = ImageNode(self, (slw, 0), (H, H), cbsrf)
        self.add(self.checkerboard)
        
        self.view = pg.Surface((H, H), pg.SRCALPHA)
        self.vx, self.vy = (slw, 0)

        self.vos.input.text = ""

    def update(self):
        inp = self.vos.input
        if inp.text:
            try:
                self.last_slider.value = int(str(self.last_slider.value)+inp.text)
                if self.last_slider.value > 255:
                    self.last_slider.value = 0
                self.last_slider.on_change(self.last_slider.value)
            except ValueError:pass
            inp.text = ""
        
        color = tuple([slider.value for slider in self.sliders])
        self.color = color
        self.view.fill(color)
        super().update()

    def render(self):
        self.render_nodes()
        super().render()
        self.vos.srf.blit(self.view, (self.x+self.vx, self.y+self.vy))

    def minimize(self):
        self.close()

    def close(self):
        if self.callback:self.callback(self.color)
        super().close()
