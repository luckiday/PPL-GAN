from tensorflow.core.protobuf import meta_graph_pb2
from collections import defaultdict
from utils import Graph, bGraph
from z3 import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("meta", nargs='?', default="check_string_for_empty")
args = parser.parse_args()

meta_graph = meta_graph_pb2.MetaGraphDef()
input_file_name = args.meta#"myGraph.meta"
with open(input_file_name, 'rb') as fin:
    file_content = fin.read()
meta_graph.ParseFromString(file_content)
graph = meta_graph.graph_def

mg = Graph(len(graph.node))
nodeIdMap={}
idNodeMap={}
predIdMap={}
idx = 0
for node in graph.node:
  nodeIdMap[node.name] = idx
  idNodeMap[idx] = node
  idx=idx+1

for node in graph.node:
  nid = nodeIdMap[node.name]
  predIdMap[nid]=[]

for node in graph.node:
  nid = nodeIdMap[node.name]
  for pred in node.input:
    pid = nodeIdMap[pred]
    mg.addEdge(pid, nid)
    predIdMap[nid].append(pid)

st = mg.topologicalSort()

bg = bGraph(mg, st[-1], nodeIdMap, idNodeMap, predIdMap)
dist = bg.compute(st[-1])
for val in dist.keys():
    print("E[Output=",val,"] = ",dist[val], sep="")

'''
dist_req = defaultdict()
dist_req[RealVal(0)] = RealVal(0.15)
dist_req[RealVal(1)] = RealVal(0.50)
dist_req[RealVal(2)] = RealVal(0.35)
res = bg.regroup(dist, 3)
bg.match(dist, res, dist_req)
'''

