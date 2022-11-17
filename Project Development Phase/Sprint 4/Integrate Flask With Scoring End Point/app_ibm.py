import requests
import warnings
import numpy as np
import json
warnings.filterwarnings('ignore')
from flask import Flask, redirect, url_for, render_template, request

#importing the inputScript file used to analyze the URL
#import inputScript

from inputScript import FeatureExtraction

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "nBfujEzb10fLXSIhI5oQ8wmrWTQ1OdPVqto5U1I-V2Ur"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

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
        z = np.array(ob.getFeaturesList()).reshape(1,30).tolist()

        payload_scoring = {"input_data": [{"fields": z, "values":z}]}
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7a90cba9-2576-4401-9aab-d73d52f05141/predictions?version=2022-11-14', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        predictions=response_scoring.json()
        print(predictions)
        predict = predictions['predictions'][0]['values'][0][0]
        if(predict==1): 
            return render_template('get_started.html',prediction_text="It is Legitimate safe website",url=url)
        else:
            return render_template('get_started.html',prediction_text="It is a phishing Website",url=url)
        
    else:
        return render_template('get_started.html')


#about page for the project
@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug = True)