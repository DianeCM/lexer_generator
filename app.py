from flask import Flask
from flask import render_template
from flask import request
from tools.regex import *
tokens={}
app = Flask(__name__)

#DOTstring1 = 'digraph G {margin=0.1;rankdir=LR;start [height=0, label="", shape=plaintext, width=0];0 [shape=circle, style=""];0 [shape=circle, style=""];0 -> 0  [id="0 a 0", label=a, labeldistance=2];0 [shape=circle, style=""];0 [shape=circle, style=""];0 -> 0  [id="0 b 0", label=b, labeldistance=2];1 [shape=circle, style=""];0 -> 1  [id="0 b 1", label=b, labeldistance=2];1 [shape=circle, style=""];2 [shape=circle, style=bold];1 -> 2  [id="1 a 2", label=a, labeldistance=2];start -> 0  [label="", style=dashed];}';
#DOTstring2 = 'digraph G {margin=0.1;rankdir=LR;start [height=0, label="", shape=plaintext, width=0];0 [shape=circle, style=""];0 [shape=circle, style=""];0 -> 0  [id="0 a 0", label=a, labeldistance=2];0 [shape=circle, style=""];1 [shape=circle, style=""];0 -> 1  [id="0 b 1", label=b, labeldistance=2];1 [shape=circle, style=""];2 [shape=circle, style=bold];1 -> 2  [id="1 a 2", label=a, labeldistance=2];1 [shape=circle, style=""];1 [shape=circle, style=""];1 -> 1  [id="1 b 1", label=b, labeldistance=2];2 [shape=circle, style=bold];0 [shape=circle, style=""];2 -> 0  [id="2 a 0", label=a, labeldistance=2];2 [shape=circle, style=bold];1 [shape=circle, style=""];2 -> 1  [id="2 b 1", label=b, labeldistance=2];start -> 0  [label="", style=dashed];}'
#tokens_automatons= [DOTstring1,DOTstring2]

@app.route('/tokens_automaton')
def tokens_automaton(name=None):
    tokens_automaton = [Regex(regular_expression).dfa().graph() for regular_expression in tokens.values()]
    return render_template('tokens_automaton.html',tokens=tokens,tokens_automaton=tokens_automaton)

@app.route('/',methods=['POST','GET'])
def tokens_table(name=None):
    if request.method == 'POST':
       tokens[request.form['type']] = request.form['regular_expression']
    #else: tokens={}
    return render_template('index.html',tokens=tokens)