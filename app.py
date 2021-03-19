import numpy as np
from flask import Flask, request, jsonify, render_template


from joblib import load
app = Flask(__name__)
model = load('LRmodel.joblib')

@app.route('/')
def index():
    return render_template('intro.html')

@app.route('/predict')
def predict():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    
    x_test = [[x for x in request.form.values()]]
    
    for i in range(4):
        x_test[0][i]=int(x_test[0][i])
    x_test[0][-2]=float(x_test[0][-2])
    x_test[0][-1]=int(x_test[0][-1])
    
    print(x_test)
    prediction = model.predict(x_test)
    print(prediction)
    output=prediction[0]
    
    l=['','','']
    areas=['Aptitude Skills','Grammar','Coding Skills','Logical Skills']
    if output==1:
        status="You have high chances of getting placed!"
        ati="Keep practising and try out new problems to keep yourself updated"
        
    else:
        status="You need to work hard to get placed"
        ati="Areas to Improve:"
        scores=sorted(x_test[0][0:4])
        for i in range(3):
            for j in range(4):
                if scores[i]==x_test[0][j] and areas[j] in l:
                    continue
                elif scores[i]==x_test[0][j]:
                    l[i]=areas[j]
        
    return render_template('index.html', prediction_text=status,areas=ati,fa=l[0],sa=l[1],ta=l[2])


if __name__ == "__main__":
    app.run(debug=False)