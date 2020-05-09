import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib
import pandas as pd
import numpy as np


#columns for the preprocessed data in model.ipynb
col = ['trans', 'origin', 'engine', 'year', 'brand_honda', 'brand_lexus',
        'brand_mercedes-benz', 'brand_toyota', 'brand_volkswagen',
        'model_accord coupe ex-l v-6 automatic',
        'model_avensis 2.4 exclusive automatic', 'model_avensis verso',
        'model_c350', 'model_camry', 'model_camry 2.4 se automatic',
        'model_corolla', 'model_corolla automatic',
        'model_corolla le 4-speed automatic', 'model_corolla le automatic',
        'model_cr-v', 'model_e350', 'model_es 330', 'model_es 350',
        'model_glk 350', 'model_gx 470 sport utility', 'model_hiace',
        'model_highlander limited v6 4x4', 'model_lt', 'model_matrix',
        'model_rav4', 'model_rav4 4wd', 'model_rav4 limited', 'model_rx',
        'model_rx 330 4wd', 'model_sienna', 'model_venza']




app = Flask(__name__)

#Rount for the home page
@app.route('/')
def home():
    return render_template('index.html')


#API to get the prediction
@app.route('/predict',methods=['POST'])
def predict():
    
    #set an empty test set with one role and 36 columns using 
    #col above as the column names
    test = pd.DataFrame([np.zeros(36)], columns=col)
    
    #use request.form to get the values of the html form
    int_features = [str(x) for x in request.form.values()]
    
    #the the month from the first index
    month = int_features[0]
    
    #deserialise the pickled model, selecting by month
    model = pickle.load(open(month+'.pkl', 'rb'))

    #populate test data from user inputs
    test['trans'] = int(int_features[1])
    test['origin'] = int(int_features[2])
    test['engine'] = int(int_features[3])
    test['year'] = int(int_features[4])
    test['brand_'+int_features[5]] = 1
    test['model_'+int_features[6]] = 1
    
    #run prediction with the model on the test data
    prediction = model.predict(test)
    output = int(prediction[0]) 
    
    #assign the output message
    message = "Used " + int_features[4] + " " + int_features[5].upper()+ " " + int_features[6].upper()+' in Nigeria is expected to range from ₦{} to ₦{}. It is safe to buy or sell at this price range'.format(output, output+100000)
    
    #the output of this API
    return render_template('index.html', prediction_text= message)




if __name__ == "__main__":
    app.run(debug=True)
