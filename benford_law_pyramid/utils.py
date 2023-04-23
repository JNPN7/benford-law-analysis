# some utility functions here 
import pandas as pd 
import numpy as np

def isnumeric(x):
    try:
        x = int(x)
        return True 
    except:
        return False 
    

def get_data_distribution(filepath):
    df = pd.read_csv(filepath)
    df['leading_digit'] = df.iloc[:,0].apply(lambda x:str(x)[0])
    leading_digits_count = df['leading_digit'].value_counts()
    leading_digits_dict = leading_digits_count.to_dict()
    filtered_dict = {}
    for k in leading_digits_dict:
        if isnumeric(k):
            if int(k) > 0:
                filtered_dict[k] = leading_digits_dict[k]
    probability_dict = {int(k): filtered_dict[k]/sum(filtered_dict.values()) for k in filtered_dict.keys()}
    return probability_dict


def check_benford_law(filepath):
    benford_distribution = {k: np.log10(1+(1/k)) for k in range(1,10)}
    observed_distribution = get_data_distribution(filepath)
    
    # chi square test
    threshold_chi_square = 15.15 # for level of significane 0.05 and no of classes 9
    calculated_chi_square = 0
    for i in range(1, 10):
        calculated_chi_square += ((observed_distribution[i] - benford_distribution[i])**2 / benford_distribution[i]) * 100

    if calculated_chi_square > threshold_chi_square:
        return False
    
    return True
