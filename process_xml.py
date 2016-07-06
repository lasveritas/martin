import xml.etree.ElementTree as ET
import sys
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

tree = ET.parse(sys.argv[1])
root = tree.getroot()

names_dict = []
unique_names = Counter()
all_names = 0
  
for child in root.iter('Name'):
  if "<" not in child.attrib['val']:
    names_dict.append([child.attrib['val'], child.attrib['pos'], child.attrib['len']])  
    unique_names[child.attrib['val']] += 1
    all_names += 1
  else:
    names_dict.append(["title", child.attrib['val'].replace("<",""), child.attrib['pos'], child.attrib['len']])
   
WORD_WINDOW=15 
def dist(line):
  line = line.split()
  if (len(line)-2) > WORD_WINDOW:
    return False
  else:
    return True
  
pairs = Counter() 
  
with open(sys.argv[2]) as f:
  text = f.read()
  for el in range(len(names_dict)-1):
    for el2 in range(el+1, len(names_dict)):
      if names_dict[el][0] != names_dict[el2][0]:
        if names_dict[el][0] != 'title' and names_dict[el2][0] != 'title':
          name1, pos1, len1 = names_dict[el]
          name2, pos2, len2 = names_dict[el2]
          print((name1, name2))
        
          text_extract = text[int(pos1):(int(pos2)+int(len2))]
          if dist(text_extract):
            pair = (max(name1, name2), min(name1, name2))
            pairs[pair] += 1
          else:
            break
        else:
          break

G=nx.Graph()
weights = []

for el in sorted(pairs.items(), key=lambda (k, v):v, reverse=True):
  if el[1]> 4:
    el1 = el[0][0]
    el2 = el[0][1]
    G.add_nodes_from([el1, el2], labels = [el1, el2])
    G.add_edges_from([(el1, el2)])    
    weights.append(el[1])

    
weights2=[]    
for i in weights:    
  if (i/float(weights[0]))>0.1:
    weights2.append(2)
  elif (i/float(weights[0]))>0.04:  
    weights2.append(1)
  else:
    weights2.append(0.5)
  
d = nx.degree(G)

nx.draw(G, nodelist=d.keys(), with_labels=True, node_size=[unique_names[x] for x in d.keys()], edge_color="#DBDBDB", node_color="#ADEDA2", width=weights2)

plt.savefig(sys.argv[3])
plt.show()





    