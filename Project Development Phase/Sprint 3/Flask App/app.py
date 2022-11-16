import pickle
import warnings
import numpy as np
warnings.filterwarnings('ignore')
from flask import Flask, redirect, url_for, render_template, request

#importing the inputScript file used to analyze the URL
#import inputScript

from inputScript import FeatureExtraction

app = Flask(__name__)
model = pickle.load(open('Phishing_website.pkl', 'rb'))

#Home page for the project
@app.route('/')
def home():
    return render_template('home.html')

#Redirects to the page to give the user input URL
@app.route('/prediction_page')
def get_started():
    return redirect(url_for('predict'))

#Fetches the URL given by the user and passes to inputScript
@app.route('/predict', methods=['GET','POST'])
def predict():
    ''' 
    for rendering results on HTML GUI
    '''
    if request.method=='POST':
        url = request.form['url']
        ob = FeatureExtraction(url)
        z = np.array(ob.getFeaturesList()).reshape(1,30)
        y_pred=model.predict(z)[0]
        c=model.predict_proba(z)[0,0]
        f=model.predict_proba(z)[0,1]
        if(y_pred==1):
            return render_template('get_started.html',prediction_text="It is Legitimate safe website",pred=y_pred,url=url)
        else:
            return render_template('get_started.html',prediction_text="It is a phishing Website",pred=y_pred,url=url)
        
    else:
        return render_template('get_started.html')

#contact page for the project
@app.route('/contact')
def contact():
    return render_template('contact.html')

#about page for the project
@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug = True)