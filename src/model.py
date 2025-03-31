import joblib
import pandas as pd

class Model:
    def __init__(self):
        self.model = joblib.load('models/catboost.pkl')
        self.scalar = joblib.load('models/StdScalar.pkl')
        # self.scalar_tenure = joblib.load('models/StdScalar_TenureMthFee.pkl')
        # self.scalar_gb = joblib.load('models/StdScalar_AvgMthlyGBDownload.pkl')
        # self.scalar_dist = joblib.load('models/StdScalar_AvgMthlyLongDistFee.pkl')

    def standard_scaling(self, total_monthly_fee, avg_gb_download_monthly, avg_long_distance_fee_monthly):
        ['total_monthly_fee', 'avg_gb_download_monthly', 'avg_long_distance_fee_monthly', 'population']
        df = pd.DataFrame([{
            'total_monthly_fee': total_monthly_fee,
            'avg_gb_download_monthly': avg_gb_download_monthly,
            'avg_long_distance_fee_monthly': avg_long_distance_fee_monthly
        }])
        return self.scalar.transform(df)[0]  
    
    def validate_float(self, field_name, error_message, errors):
        try:
            return float(field_name)
        except (ValueError, KeyError):
            errors.append(error_message)
            return None


    def validate_int(self, field_name, error_message, errors):
        try:
            return int(field_name)
        except (ValueError, KeyError):
            errors.append(error_message)
            return None

    # def standard_scaling_tenure(self, input_var):
    #     return self.scalar_tenure.transform([[input_var]])[0][0]
    
    # def standard_scaling_gb(self, input_var):
    #     return self.scalar_gb.transform([[input_var]])[0][0]

    # def standard_scaling_dist(self, input_var):
    #     return self.scalar_dist.transform([[input_var]])[0][0]

    def predict(self, input_features):
        return self.model.predict(input_features)
