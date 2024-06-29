from vos import *
from math import sqrt

class MyApp(WindowApp):
    def __init__(self, vos):
        super().__init__(vos, "Resizer", vos.res)
        self.desktop = False

    def run(self, target=None):
        app = super().run()
        app.target = target
        app.srf.set_alpha(200)
        app.redraw()

    def update(self):
        inp = self.vos.input
        
        if inp.click_inst:
            ax, ay, w, h = self.target.rect
            bx, by = ax+w, ay+h
            mx, my = self.mouse
            ad = sqrt((ax-mx)**2+(ay-my)**2)
            bd = sqrt((bx-mx)**2+(by-my)**2)
            if ad < bd:
                ax, ay = mx, my
            else:
                bx, by = mx, my
            if ax > bx: ax, bx = bx, ax
            if ay > by: ay, by = by, ay
            w, h = bx - ax, by - ay
            w = max(50, w)
            h = max(50, h)
            self.target.resize((w, h))
            self.target.render()
            self.target.x, self.target.y = ax, ay
            self.redraw()

        if pg.K_RETURN in inp.keys:
            self.close()
            self.target.focus()
            
    def redraw(self):            
        self.srf.fill((0,0,0))
        pg.draw.rect(self.srf, (255,255,255), self.target.rect)
