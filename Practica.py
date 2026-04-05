import pickle

preprocessor_path = "artifact/02_08_2026_15_52_40/data_transformation/transformed_object/preprocessing.pkl"


with open(preprocessor_path, "rb") as f1:
    preprocessor = pickle.load(f1)

print(preprocessor)
        