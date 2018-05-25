from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    from random import randint
    from sqlalchemy import create_engine
    import pandas as pd
    import numpy as np
    from sklearn.neighbors import KNeighborsClassifier

    red_train = randint(0,255)
    green_train = randint(0,255)
    blue_train = randint(0,255)

    # Predicting data
    engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/colors_predictor')
    conn = engine.connect()
    sql_query = "SELECT * from colors"
    result = conn.execute(sql_query)
    rows = result.fetchall()
    if len(rows) > 10:
        df = pd.DataFrame(rows, columns=['red','green','blue','foreground'])
        model = KNeighborsClassifier(n_neighbors=3, n_jobs=1)
        model.fit(df[['red','green','blue']], df[['foreground']])

        df2 = pd.DataFrame({
            'red': red_train,
            'green': green_train,
            'blue': blue_train,
        }, index=[0], columns=['red','green','blue'])

        pred = model.predict(df2[['red','green','blue']])
    conn.close()

    # Inserting into dataset
    answer = request.form.get('answer')
    if answer is not None:
        red = request.form.get('red')
        green = request.form.get('green')
        blue = request.form.get('blue')
        
        engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/colors_predictor')
        conn = engine.connect()
        sql_query = "INSERT INTO colors VALUES("+red+", "+green+", "+blue+", '"+answer+"')"
        conn.execute(sql_query)
        conn.close()


    return render_template('index.html', red=red_train, green=green_train, blue=blue_train, pred=pred, test = len(rows))

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
