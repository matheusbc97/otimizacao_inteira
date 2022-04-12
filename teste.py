import gurobipy as gp 
from gurobipy import GRB

m = gp.Model("mp1")

x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

m.setObjective(x+y+2*z, GRB.MAXIMIZE)

m.addConstr(x + 2*y + 3*z <=4, "c0")
m.addConstr(x + y >=1, "c1")

m.optimize()
