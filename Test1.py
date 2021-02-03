from flask import Flask,request,render_template,redirect,flash
from flask_restful import Api, Resource
from collections import defaultdict,Counter
import math 
import string 
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
api = Api(app)
result = 0 

@app.route('/')
def my_form():
    return render_template("front.html") 

@app.route('/files',methods=["GET","POST"])
def tf_idf():
    if request.method == 'POST':

        req = request.form
        file1 = req["file1"]
        file2 = req["file2"]
        files = [file1,file2]
        dic = []
        for i in files:
            try:
                f = open(i+".txt","r")
                s = f.read()
                d = defaultdict(int)
                for j in s.split():
                    if j in string.punctuation:
                        continue
                    else:
                        d[j]+=1
                dic.append(d)
                f.close()
            except FileNotFoundError:
                flash(f'The File {i} you have entered is not in the directory')
                return render_template("front.html")
        result = cosine_similarity(dic[0],dic[1])

    return render_template("front.html",result = "%.2f" % result)

def dotProduct(D1, D2):  
    Sum = 0.0
    for key in D1: 
        
        if key in D2: 
            Sum += (D1[key] * D2[key]) 
            
    return Sum

def cosine_similarity(D1, D2):  
    numerator = dotProduct(D1, D2) 
    denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2)) 
    
    return (numerator / denominator)


if __name__ == '__main__':
    app.run(debug=True)