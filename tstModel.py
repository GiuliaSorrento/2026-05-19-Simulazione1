from model.model import Model

mm = Model()
mm.buildGraph(1)

n,a = mm.getGraphDetails()
print(n,a)

nodoInf, maxInf, archi = mm.getDettagli()
print(f"nodo + influente: {nodoInf}, valore: {maxInf}")
for e in archi:
    print(f"{e[0]},{e[1]},{e[2]["weight"]}")