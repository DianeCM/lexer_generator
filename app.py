from flask import Flask,render_template,request,redirect,url_for
from tools.regex import *
from tools.lexer import *
tokens={}
app = Flask(__name__)
transitions=[]
token_index=0
tran_index=0
lex=None
automaton=None
token_transitions=[]

@app.route('/',methods=['POST','GET'])
def tokens_table(name=None):
    global tokens
    if request.method == 'POST':
       tokens[request.form['type']] = request.form['regular_expression']
    #else: tokens={}
    return render_template('index.html',tokens=tokens)

@app.route('/tokens_automaton/<graph>',methods=['POST','GET'])
def tokens_automaton(graph):
   return render_template('tokens_automaton.html',graph=graph)

@app.route('/get_graph/<regular_exp>',methods=['POST','GET'])
def get_graph(regular_exp):
    graph=Regex(regular_exp)._dfa().graph()
    return redirect(url_for('tokens_automaton',graph=graph))

@app.route('/tokenizer/<action>',methods=['POST','GET'])
def tokenizer(action):
   global lex
   global token_index
   global transitions
   global automaton
   global tran_index
   global token_transitions
   if action=='start':
      table=[ (type,reg_exp) for type,reg_exp in tokens.items()]
      lex=Lexer(table,'$')
      automaton=lex.automaton.graph()
      #return render_template('tokenizer.html',automaton=automaton,origin="",symbol="",end="")
      return render_template('tokenizer.html',automaton=automaton,transitions=[])
   elif action == 'save':
      if request.method=='POST':
         token_index=0
         tran_index=0
         transitions=lex(request.form['text'])
         token_transitions = transitions[0]
         return render_template('tokenizer.html',automaton=automaton,transitions=transitions)
   return render_template('tokenizer.html',automaton=automaton,transitions=[])
