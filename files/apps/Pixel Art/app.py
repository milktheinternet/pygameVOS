from vos import *
from math import floor

class Canvas(SurfaceNode):
    def __init__(self, app, size=(600, 600), cnvsize=(32,32), cb1=(100,100,100), cb2=(120,120,120)):
        super().__init__(app, size=size)
        self.cnv = pg.Surface(cnvsize, pg.SRCALPHA)
        self.cnv.fill((0, 0, 0, 0))
        self.cnvw, self.cnvh = cnvsize

        self.checkerboard = pg.Surface(cnvsize)
        self.checkerboard.fill(cb1)
        for x in range(self.cnvw):
            for y in range(self.cnvh):
                if x%2==y%2:
                    self.checkerboard.set_at((x,y), cb2)
        self.checkerboard = pg.transform.scale(self.checkerboard, self.size)

    def draw(self, color=(0,0,0,255)):
        x, y = self.app.mouse
        gx, gy = self.global_pos
        x = floor((x - gx)/self.size[0]*self.cnvw)
        y = floor((y - gy)/self.size[1]*self.cnvh)
        if 0 <= x < self.cnvw and 0 <= y < self.cnvh:
            self.cnv.set_at((x,y), color)

    def render(self):
        self.srf.blit(self.checkerboard, (0,0))
        self.srf.blit(pg.transform.scale(self.cnv, self.size), (0,0))
        super().render()

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "Pixel Art", (800, 600))
        self.bg = (10, 10, 10)
        self.bg2 = (33, 33, 33)
        self.color = (200,200,200)
        self.font = self.vos.load_font(size=17)

        self.draw_color = (0,0,0,255)

    def on_run(self):
        super().on_run()
        self.setup_nodes()

    def setup_nodes(self):
        self.children = []

        self.cnv = Canvas(self, tuple([min(self.res)]*2), (32, 32))
        self.add(self.cnv)

        button_data = {
            "save":lambda:None,
            "open":lambda:None,
            "color":lambda:None,
            "pen":lambda:None,
            "line":lambda:None,
            "bucket":lambda:None,
            "fullscreen":lambda:None
            }
        
        btn_w = self.res[0] - self.cnv.size[0]
        btn_h = self.res[1] / len(button_data)

        x, y = self.cnv.size[0], 0

        for text, on_press in button_data.items():
            btn = ButtonNode(self, pos=(x,round(y)), size=(btn_w, btn_h), text = text, center=True, on_press = on_press, font = self.font)
            self.add(btn)
            y += btn_h

    def update(self):
        inp = self.vos.input
        if inp.click:
            self.cnv.draw(self.draw_color)

    def render(self):
        self.srf.fill(self.bg)
        self.render_nodes()
        super().render()
