from virtualOS import pg, WindowApp

PATTERNS = (
    ((1,1,1),(0,0,0),(0,0,0)),
    ((0,0,0),(1,1,1),(0,0,0)),
    ((0,0,0),(0,0,0),(1,1,1)),
    ((1,0,0),(1,0,0),(1,0,0)),
    ((0,1,0),(0,1,0),(0,1,0)),
    ((0,0,1),(0,0,1),(0,0,1)),
    ((1,0,0),(0,1,0),(0,0,1)),
    ((0,0,1),(0,1,0),(1,0,0))
    )

class MyApp(WindowApp):
    def __init__(self, name, vos, resolution = (32*3+80, 32*3+80)):
        super().__init__(name, vos, resolution)
        self.bg = (10,10,10)
        self.fg = (100,100,100)
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        self.X_IMG = self.load_image("X.png")
        self.O_IMG = self.load_image("O.png")
        self.margin = 20
        self.gridsz = self.margin//5
        self.SZ = 32#(32 - self.margin * 4)//3
        self.turn = 1
        def resize(img):
            return pg.transform.smoothscale(img, (self.SZ, self.SZ))
        self.X_IMG = resize(self.X_IMG)
        self.O_IMG = resize(self.O_IMG)
        self.winner = None
        self.font = pg.font.SysFont('helvetica', 40)
        self.stop_rendering = False
    def render(self):
        super().render()
        if self.stop_rendering:
            return
        if self.winner == None:
            self.srf.fill(self.bg)
            for x in range(3):
                if x < 2:
                    pg.draw.rect(self.srf, self.fg, ((x+1)*(self.SZ + self.margin) + self.margin//2-self.gridsz//2, self.margin,
                                                     self.gridsz, self.res[1]-self.margin*2))
                    pg.draw.rect(self.srf, self.fg, (self.margin, (x+1)*(self.SZ + self.margin) + self.margin//2-self.gridsz//2,
                                                     self.res[0]-self.margin*2, self.gridsz))
                for y in range(3):
                    if self.grid[y][x]:
                        self.srf.blit([None, self.X_IMG, self.O_IMG][self.grid[y][x]], (x*(self.SZ + self.margin) + self.margin,
                                               y*(self.SZ + self.margin) + self.margin))
        else:
            self.stop_rendering = True
            self.srf.fill(self.bg)
            msg = self.font.render(["TIE", "X WINS", "O WINS"][self.winner], True, (255,255,255))
            
            self.srf.blit(msg, (self.res[0]//2-msg.get_width()//2,self.res[1]//2-msg.get_height()//2))
        
    def check_win(self):
        for turn in (1, -1):
            if True not in [0 in self.grid[y] for y in range(3)]:
                self.winner = 0
            for pattern in PATTERNS:
                nwin = 0
                for x in range(3):
                    for y in range(3):
                        if self.grid[y][x]==turn and pattern[y][x]:
                            nwin += 1
                if nwin == 3:
                    self.winner = turn
    def update(self):
        if not self.visible:return
        super().update()
        if self.winner:
            return
        inp = self.vos.input
        mx, my = inp.mouse
        mx -= self.pos[0] + self.margin//2
        mx //= self.SZ + self.margin
        my -= self.pos[1] + self.margin//2
        my //= self.SZ + self.margin
        if inp.click_inst and 0 <= mx < 3 and 0 <= my < 3 and not self.grid[my][mx]:
            self.grid[my][mx] = self.turn
            self.turn *= -1
            self.check_win()
