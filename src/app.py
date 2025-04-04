from flask import Flask, request, render_template
import joblib
from model import Model
import numpy as np
import re

app = Flask(__name__)

# Method 1: via HTMML Form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        inputs_dict = dict(request.form)
        print(inputs_dict)
        errors = []

        contract_type = inputs_dict['contract_type']
        num_dependents_bin = inputs_dict['num_dependents_bin']
        num_referrals_bin = inputs_dict['num_referrals_bin']

        total_monthly_fee_raw = inputs_dict['total_monthly_fee_raw']
        tenure_months = inputs_dict['tenure_months']
        avg_long_distance_fee_monthly_raw = inputs_dict['avg_long_distance_fee_monthly_raw']
        total_charges_quarter = inputs_dict['total_charges_quarter']
        avg_gb_download_monthly_raw = inputs_dict['avg_gb_download_monthly_raw']

        total_monthly_fee_raw = Model().validate_float(total_monthly_fee_raw, "Total Monthly Fee must be a valid number.", errors)
        tenure_months = Model().validate_int(tenure_months, "Tenure Months must be a valid integer.", errors)
        avg_long_distance_fee_monthly_raw = Model().validate_float(avg_long_distance_fee_monthly_raw, "Average Long Distance Fee must be a valid number.", errors)
        total_charges_quarter = Model().validate_float(total_charges_quarter, "Total Charges for Quarter must be a valid number.", errors)
        avg_gb_download_monthly_raw = Model().validate_float(avg_gb_download_monthly_raw, "Average GB Download Monthly must be a valid number.", errors)

        # total_monthly_fee_raw = float(inputs_dict['total_monthly_fee_raw'])
        # tenure_months = int(inputs_dict['tenure_months'])
        # avg_long_distance_fee_monthly_raw = float(inputs_dict['avg_long_distance_fee_monthly_raw'])
        # total_charges_quarter = float(inputs_dict['total_charges_quarter'])
        zip_code_full = inputs_dict['zip_code_full']
        if not re.fullmatch(r"\d{6}", zip_code_full):
            errors.append("Invalid Zip Code. It must be exactly 6 digits.")

        payment_method = inputs_dict['payment_method']


        if errors:
            return render_template("home.html", errors=errors, form_data=inputs_dict)

        # Pre-processing of input data
        total_monthly_fee, avg_gb_download_monthly,  avg_long_distance_fee_monthly=  Model().standard_scaling(total_monthly_fee_raw, avg_gb_download_monthly_raw, avg_long_distance_fee_monthly_raw)
        # total_monthly_fee =  Model().standard_scaling_tenure(total_monthly_fee_raw)
        # avg_gb_download_monthly =  Model().standard_scaling_gb(avg_gb_download_monthly_raw)
        # avg_long_distance_fee_monthly = Model().standard_scaling_dist(avg_long_distance_fee_monthly_raw)
        total_charges_quarter_cbrt = np.cbrt([total_charges_quarter])[0]
        zip_code = str(zip_code_full)[:2]

        # Get the parameters for the prediction
        parameters = [contract_type, num_dependents_bin, num_referrals_bin,
                       total_monthly_fee, tenure_months, avg_gb_download_monthly, 
                       total_charges_quarter_cbrt, zip_code,
                       payment_method, avg_gb_download_monthly]


        # Make a binary prediction
        prediction = Model().predict(parameters)

            # Return the result along with the form
        return render_template('results.html', prediction=prediction)

    # If it's a GET request, just render the form
    return render_template('home.html')

# Method 2: via API
@app.route('/api/predict', methods=['POST'])
def predict():
    request_data = request.get_json()
    print(request_data)

    contract_type = request_data['contract_type']
    num_dependents_bin = request_data['num_dependents']
    num_referrals_bin = request_data['num_referrals']
    total_monthly_fee_raw = request_data['total_monthly_fee']
    tenure_months = request_data['tenure_months']
    avg_long_distance_fee_monthly_raw = request_data['avg_long_distance_fee_monthly']
    total_charges_quarter = request_data['total_charges_quarter']
    zip_code_full = request_data['zip_code']
    payment_method = request_data['payment_method']
    avg_gb_download_monthly_raw = request_data['avg_gb_download_monthly']

    # Pre-processing of input data
    total_monthly_fee, avg_gb_download_monthly,  avg_long_distance_fee_monthly=  Model().standard_scaling(total_monthly_fee_raw, avg_gb_download_monthly_raw, avg_long_distance_fee_monthly_raw)
    # total_monthly_fee =  Model().standard_scaling_tenure(total_monthly_fee_raw)
    # avg_gb_download_monthly =  Model().standard_scaling_gb(avg_gb_download_monthly_raw)
    # avg_long_distance_fee_monthly = Model().standard_scaling_dist(avg_long_distance_fee_monthly_raw)
    total_charges_quarter_cbrt = np.cbrt([total_charges_quarter])[0]
    zip_code = str(zip_code_full)[:2]

    # # Get the parameters for the prediction
    parameters = [contract_type, num_dependents_bin, num_referrals_bin,
                    total_monthly_fee, tenure_months, avg_gb_download_monthly, 
                    total_charges_quarter_cbrt, zip_code,
                    payment_method, avg_gb_download_monthly
                    ]

    # Make a binary prediction
    prediction = int(Model().predict(parameters))
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(debug=True)