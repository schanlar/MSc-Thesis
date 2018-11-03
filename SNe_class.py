"""
@author Savvas Chanlaridis
@version 29/10/2018

The script creates a tree diagram for Supernovae classification

"""




from graphviz import Digraph

dot = Digraph(name = 'SNe classification')

dot.node("A", "Spectral Lines", style = "filled", fillcolor = "wheat")
dot.node("B", "Hydrogen", style = "filled", fillcolor = "wheat")
dot.node("C", "No Hydrogen", style = "filled", fillcolor = "wheat")
dot.node("D", "Type II", color = "red", style = "filled", fillcolor = "wheat", fontname="times-bold")
dot.node("E", "Silicon", style = "filled", fillcolor = "wheat")
dot.node("F", "No Silicon", style = "filled", fillcolor = "wheat")
dot.node("G", "Type Ia", color = "blue", style = "filled", fillcolor = "wheat", fontname="times-bold")
dot.node("H", "Helium", style = "filled", fillcolor = "wheat")
dot.node("I", "No Helium", style = "filled", fillcolor = "wheat")
dot.node("J", "Type Ib", color = "red", style = "filled", fillcolor = "wheat", fontname="times-bold")
dot.node("K", "Type Ic", color = "red", style = "filled", fillcolor = "wheat", fontname="times-bold")





dot.edges(["AB", "AC"])
dot.edges(["BD"])
dot.edges(["CE", "CF"])
dot.edges(["EG"])
dot.edges(["FH", "FI"])
dot.edges(["HJ", "IK"])


dot.graph_attr['rankdir'] = 'LR'
dot.edge_attr.update(arrowhead = 'none')






dot.format = 'pdf'
dot.render("SNeClass-output/SNeClass.gv", view = True)
