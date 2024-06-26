from virtualOS import *
from random import choice

class Ball(RectNode):
    def __init__(self, app, pos, size=(10,10), color=(255,255,255)):
        super().__init__(app, pos, size, color)
        self.speed = 5
        self.init_pos = pos
        self.reset_ball()
    def reset_ball(self):
        self.vx, self.vy = (choice([-1,1]), choice([-1,1]))
        self.x, self.y = self.init_pos
    def update(self):
        self.x += self.vx
        self.y += self.vy
    

class Paddle(RectNode):
    def __init__(self, app, pos=(0,0), size=(10,50), color=(255,255,255), inputs=[pg.K_UP, pg.K_DOWN]):
        super().__init__(app, pos, size, color)
        self.inps = inputs
        self.speed = 5
    def update(self):
        super().update()
        if self.inps[0] in self.vos.input.keys: # up
            self.y -= self.speed
        if self.inps[1] in self.vos.input.keys: # down
            self.y += self.speed
        self.y = max(0,min(self.y, self.app.res[1]-self.size[1]))

class MyApp(NodeApp):
    def __init__(self, name, vos, resolution=(400, 400)):
        super().__init__(name, vos, resolution)
        self.init_res = resolution
        self.setup_nodes()

    def setup_nodes(self):
        self.children = []
        self.left = Paddle(self,(self.res[0]-10, 0))
        self.add(self.left)
        self.right = Paddle(self, inputs=[pg.K_w, pg.K_s])
        self.add(self.right)
        self.ball = Ball(self, [x//2-5 for x in self.res])
        self.add(self.ball)
        
        self.leftscore = TextNode(self, (0,0), (20,20), "0")
        self.add(self.leftscore)
