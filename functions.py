import pickle

def load_index():
    with open('inverted_index.pkl', 'rb') as f:
        loaded_data = pickle.load(f)

    index = loaded_data["index"]
    doc_length_dict = loaded_data["doc_length_dict"]

    return index, doc_length_dict
