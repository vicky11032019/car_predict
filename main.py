
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            present_price=float(request.form['present_price'])
            kms_driven = int(request.form['kms_driven'])
            owner = int(request.form['owner'])
            year = int(request.form['year'])
            car_age=2020-year
            fuel_type = request.form['fuel_type']
            if(fuel_type=="Petrol"):
                Fuel_Type_Diesel=0
                Fuel_Type_Petrol=1
            elif(fuel_type=="Diesel"):
                Fuel_Type_Diesel=1
                Fuel_Type_Petrol=0
            else:
                Fuel_Type_Diesel=0
                Fuel_Type_Petrol=0

            seller_type=request.form['seller_type']
            if(seller_type=="Individual"):
                Seller_Type_Individual=1
            else:
                Seller_Type_Individual=0

            transmission_type = request.form['transmission_type']
            if (transmission_type == "Manual"):
                Transmission_Manual = 1
            else:
                Transmission_Manual = 0


            filename = 'car_predict_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            #scaler= pickle.load(open("my_scaler.pickle", 'rb'))
            prediction=loaded_model.predict([[present_price, kms_driven, owner, car_age, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
            print('Car should be sold at', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(prediction[0],2))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

@app.route("/from_posting", methods=['POST'])
def from_posting():
    present_price = float(request.form['present_price'])
    kms_driven = int(request.form['kms_driven'])
    owner = int(request.form['owner'])
    year = int(request.form['year'])
    car_age = 2020 - year
    fuel_type = request.form['fuel_type']
    if (fuel_type == "Petrol"):
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 1
    elif (fuel_type == "Diesel"):
        Fuel_Type_Diesel = 1
        Fuel_Type_Petrol = 0
    else:
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 0

    seller_type = request.form['seller_type']
    if (seller_type == "Individual"):
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0

    transmission_type = request.form['transmission_type']
    if (transmission_type == "Manual"):
        Transmission_Manual = 1
    else:
        Transmission_Manual = 0

    filename = 'car_predict_model.pickle'
    loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
    # predictions using the loaded model file
    # scaler= pickle.load(open("my_scaler.pickle", 'rb'))
    prediction = loaded_model.predict([[present_price, kms_driven, owner, car_age, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                        Seller_Type_Individual, Transmission_Manual]])
    print('Car should be sold at', prediction)

    return jsonify({"Prediction": prediction[0]})


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app