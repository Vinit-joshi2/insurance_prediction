# Demo file - Just for practice purpose Don't need to use

import pickle
import dill

preprocessor_path = "preprocessing.pkl"




with open(preprocessor_path, "rb") as f1:
    preprocessor = pickle.load(f1)

print(preprocessor)



        




