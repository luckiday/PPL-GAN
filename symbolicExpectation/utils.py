#Python program to print topological sorting of a DAG
from collections import defaultdict
from z3 import *
import itertools
#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.graph = defaultdict(list) #dictionary containing adjacency List
        self.V = vertices #No. of vertices
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v)
 
    # A recursive function used by topologicalSort
    def topologicalSortUtil(self,v,visited,stack):
 
        # Mark the current node as visited.
        visited[v] = True
 
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Push current vertex to stack which stores result
        stack.insert(0,v)
 
    # The function to do Topological Sort. It uses recursive 
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False]*self.V
        stack =[]
 
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Print contents of the stack
        print(stack)
        return stack
            


class bGraph:
    def extractProb(self, v, l):
        if(self.idNodeMap[v].name.find("probs")!=-1):
            l.append(self.idNodeMap[v].attr["value"].tensor.float_val._values[0].real)
            return 
        for x in self.predIdMap[v]:
            self.extractProb(x, l)
        
    def traverse(self, v):
        print(v,self.idNodeMap[v].name)
        self.bgraph[v] = self.graph[v]
        if(self.idNodeMap[v].name.find("Bernoulli")!=-1):
            l = []
            self.extractProb(v,l)
            print("Bernoulli Prob:",l[-1])
            dist = defaultdict()
            dist[BoolVal(True)] = RealVal(l[0])
            dist[BoolVal(False)] = RealVal(1.0 - l[0])
            self.idDistMap[v] = dist
            return
        if(self.idNodeMap[v].name.find("Placeholder")!=-1):
            dist = defaultdict()
            dist[BoolVal(True)] = Real("prob")
            dist[BoolVal(False)] = RealVal(1.0)-Real("prob")
            '''for x in range(2):
                val = "val_"+str(x)
                prob = "prob_"+str(x)
                dist[Real(val)] = Real(prob)'''
            self.idDistMap[v] = dist
            return
        if(len(self.predIdMap[v])==0):
            return
        for pred in self.predIdMap[v]:
            self.traverse(pred)

    def __init__(self, Graph, v, nodeIdMap, idNodeMap, predIdMap):
        self.bgraph = defaultdict(list)
        self.idDistMap = defaultdict(dict)
        self.graph = Graph.graph
        self.nodeIdMap = nodeIdMap
        self.idNodeMap = idNodeMap
        self.predIdMap = predIdMap
        self.traverse(v)

    def my_op(self, x1, x2, name):
        if(name.find("add")!=-1):
            return x1+x2
        if(name.find("LogicalAnd")!=-1):
            return x1 and x2
        
    def compute(self, v):
        dist = defaultdict()
        opName = self.idNodeMap[v].name
        for k1 in self.idDistMap[self.predIdMap[v][0]].keys():
            for k2 in self.idDistMap[self.predIdMap[v][1]].keys():
                key = self.my_op(k1, k2, opName)
                dp = self.idDistMap[self.predIdMap[v][0]][k1]*self.idDistMap[self.predIdMap[v][1]][k2]
                if key not in dist:
                    dist[key] = dp
                else:
                    dist[key] = dist[key] + dp
        return dist
#{val_1 + 1: prob_1*1/2, val_0 + 1: prob_0*1/2, val_1 + 0: prob_1*1/2, val_0 + 0: prob_0*1/2
    def rebuild(self, res, com, v, temp, tl):
        if(v==len(com)):
            res.append(temp)
            return
        for x in list(itertools.combinations(tl, com[v].as_long())):
            tlc = list(tl)
            for item in x:
                tlc.remove(item) 
            tempc = list(temp)  
            tempc.append(list(x))
            self.rebuild(res, com, v+1, tempc, tlc)
        
        
    def regroup(self, dist, num):
        ret = []
        n = len(dist.keys())
        tl = list(dist.keys())
        varl = []
        for i in range(num):
            varl.append(Int("x"+str(i)))
        s = Solver()
        sumx = IntVal(0)
        for x in varl:
            s.add(x>=1)
            sumx = sumx + x
        s.add(sumx==n)
        s.push()
        while(s.check()==sat):
            m = s.model()
            print(m)
            com = []
            for x in m.decls():
                com.append(m[x])
            # [1,2,1]
            res=[]
            temp=[]
            self.rebuild(res, com, 0, temp, tl)
            for x in res:
                print("====\n",x)
                ret.append(x)
            for x in m.decls():
                s.add(Int(x.name())!=m[x])
        return ret


    def match(self, dist1, res, dist2):
        s = Solver()
        num = len(dist2.keys())
        kl2 = list(dist2.keys())
        for item in res:
            print("======")
            for i in range(num):
                accum = RealVal(0)
                for q in item[i]:
                    s.add(q == kl2[i])
                    print(q == kl2[i])
                    accum = accum + dist1[q]
                s.add(accum == dist2[kl2[i]])
                print(accum == dist2[kl2[i]])
            if(s.check()==unsat):
                s.reset()
                continue;
            print("===Result===")
            for x in dist1.keys():
                print("val=",x," prob=",dist1[x])
            print(s.model())
            return
            
                  
                

    
        
