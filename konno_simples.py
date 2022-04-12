import gurobipy as gp
from gurobipy import GRB

m = gp.Model("mp1")

class Acao:
    def __init__(self, codigo, rentabilidades):
        self.codigo = codigo
        self.rentabilidades = rentabilidades
        self.rentabilidadeMedia = sum(rentabilidades) / len(rentabilidades)

taxaRetornoMinimo = 1.1 # Menor taxa de retorno que o usuário quer
montanteInicial = m.addVar(800, 800, 0, vtype=GRB.INTEGER, name="montante")
tempos = 2
acoes = [Acao('MGLU3', [8.64, -2.41]), Acao('BIDI11', [1.3, -1.71])]
quantidadeAcoes = len(acoes)

# Preechimento do vetor Yt (Y em função de t)
Yt = []

for t in range(tempos):
    somatorio = 0
    for acao in acoes:
        somatorio += acao.rentabilidades[t] - acao.rentabilidadeMedia

    Yt.append(abs(somatorio))
# Fim Preechimento do vetor Yt (Y em função de t)

# Função Objetivo

somatorioFuncaoObjetivo = gp.quicksum(Yt[t] / tempos  for t in range(tempos)) 

m.setObjective(somatorioFuncaoObjetivo, GRB.MINIMIZE)
# Fim Função Objetivo

Xj = [] # vetor Xj
for index in range(len(acoes)):
    Xj.append(m.addVar(vtype=GRB.INTEGER, name="x{index}"))


# Restrição (1)

for t in range(tempos):
    somatorioRestricao1 = 0

    for j in range(quantidadeAcoes):
        Ajt = acoes[j].rentabilidades[t] - acoes[j].rentabilidadeMedia
        somatorioRestricao1 = gp.quicksum([somatorioRestricao1, Ajt *Xj[t]])

    m.addConstr(Yt[t] + somatorioRestricao1  >= 0, "r1{t}")
# Fim da restrição (1))

# Restrição (2)

for t in range(tempos):
    somatorioRestricao2 = 0

    for j in range(quantidadeAcoes):
        Ajt = acoes[j].rentabilidades[t] - acoes[j].rentabilidadeMedia
        somatorioRestricao2 = gp.quicksum([somatorioRestricao2, Ajt *Xj[t]])

    m.addConstr(Yt[t] + somatorioRestricao2  >= 0, "r2{t}")
# Fim da restrição (2))


# Restrição (3)
somatorioRestricao3 = gp.quicksum(
    acoes[j].rentabilidadeMedia * Xj[j] for j in range(quantidadeAcoes)
)

m.addConstr(somatorioRestricao3 >= taxaRetornoMinimo * montanteInicial, "r3")
# Fim Restrição (3)


# Restrição (4)
m.addConstr(sum(Xj) == montanteInicial, "r4")
# Fim Restrição (4)

# Restrição (5)
for j in range(quantidadeAcoes):
    m.addConstr(0 <= Xj[j], "r5{j}")
# Fim Restrição (5)

# Restrição (6)
for j in range(quantidadeAcoes):
    m.addConstr(Xj[j] <= 600, "r6{j}")
# Fim Restrição (6)

m.optimize()
#print(f"Optimal objective value: {m.objVal}")

for j in range(len(Xj)):
    print(f"Solution value: {acoes[j].codigo}{j}={Xj[j].X}")
