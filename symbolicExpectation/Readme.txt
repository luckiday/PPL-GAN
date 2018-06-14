target.py is the target probabilistic program we try to do the inverse inference for its input based on the given/observed output distribution. It also includes codes in the end of file export the computation graph as a proto file "myGraph.meta". "myGraph.txt" is a human-readable format describing graph structure in json.

Running instruction:
1. python target.py
2. python parse.py

Example:
x1 := Bernoulli(prob)
x2 := Bernoulli(0.5)
y := x1 /\ x2

Terminal output:
E[Output=True] = prob*1/2
E[Output=False] = prob*1/2 + (1 - prob)*1/2 + (1 - prob)*1/2 = 1 - prob*1/2
