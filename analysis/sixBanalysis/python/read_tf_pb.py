import tensorflow as tf
from tensorflow.python.platform import gfile
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i","--input")
args = parser.parse_args()

GRAPH_PB_PATH = args.input
with tf.Session() as sess:
   print("load graph")
   with gfile.FastGFile(GRAPH_PB_PATH,'rb') as f:
       graph_def = tf.GraphDef()
   graph_def.ParseFromString(f.read())
   sess.graph.as_default()
   tf.import_graph_def(graph_def, name='')
   graph_nodes=[n for n in graph_def.node]
   names = []
   for t in graph_nodes:
      names.append(t.name)
      
prompt = [
    "[File Name]---->"+args.input,
    "[Input Nodes]-->"+str(names[0])+"\n"+str(graph_nodes[0].attr),
    "[Output Nodes]->"+str(names[-1])+"\n"+str(graph_nodes[-1].attr),
    "[All Nodes]---->"+str(names)
]

print "\n".join(prompt)
