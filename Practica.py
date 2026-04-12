import pickle

preprocessor_path = "preprocessing.pkl"


with open(preprocessor_path, "rb") as f1:
    preprocessor = pickle.load(f1)

print(preprocessor)
        