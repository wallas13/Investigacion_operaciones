class Coord:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def ecuaCordCord(self, coord):
        pass
    def __eq__(self,coord):
        return coord.x == self.x and coord.y == self.y
    def __str__(self):
        return f"({self.x}, {self.y})"
    def coord_restric(self, restric):
        for res in restric:
            resizc = round(self.x*res.x + self.y*res.y,2)
            if self.x < 0 or self.y < 0:
                return False
            if res.tipo == '<=' and resizc > res.resultado:
                return False
            elif res.tipo == '>=' and resizc < res.resultado:
                return False
            elif res.tipo == '=' and resizc != res.resultado:
                return False
        return True
    def ecuaPerte(self, punt2, restricciones):
        for restric in restricciones:
            func_desp=restric.funcdesp()
            if func_desp['tipo']=='normal' and func_desp['x']*self.x + func_desp['resultado'] >= self.y-0.2 and func_desp['x']*self.x + func_desp['resultado'] <= self.y+0.2 and func_desp['x']*punt2.x + func_desp['resultado'] >= punt2.y-0.2 and func_desp['x']*punt2.x + func_desp['resultado'] <= punt2.y+0.2:
                return True
            elif func_desp['tipo']=='puntx' and func_desp['resultado']>=self.x-0.2 and func_desp['resultado']<=self.x+0.2 and func_desp['resultado']>=punt2.x-0.2 and func_desp['resultado']<=punt2.x+0.2:
                return True
            elif func_desp['tipo']=='punty' and func_desp['resultado']>=self.y-0.2 and func_desp['resultado']<=self.y+0.2 and func_desp['resultado']>=punt2.y-0.2 and func_desp['resultado']<=punt2.y+0.2:
                return True
            elif self.y == 0 and punt2.y==0:
                return True
            elif self.x==0 and punt2.x==0:
                return True
        return False
