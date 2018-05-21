from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    from random import randint
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)

    return render_template('index.html', red=r, green=g, blue=b)

@app.route('/answer', methods=['GET','POST'])
def answer():
    import pandas as pd
    answer = request.form.get('answer')
    
    red = request.form.get('red')
    green = request.form.get('green')
    blue = request.form.get('blue')
    
    df2 = pd.DataFrame({
        'Red': red,
        'Green': green,
        'Blue': blue,
        'Foreground': answer
    }, index=[0], columns=['Red','Green','Blue','Foreground'])

    df2.to_csv('colors.csv', mode='a', header=False, index=None)
   
    # return render_template('test.html', df=df)
    return redirect('/')

if __name__=='__main__':
    app.run()
