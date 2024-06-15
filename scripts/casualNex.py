
import numpy as np
from sklearn.preprocessing import LabelEncoder
from causalnex.structure.notears import from_pandas
import pickle
from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE
import warnings
from causalnex.structure import StructureModel


def listing_non_numeric_columns (data):
    non_numeric_columns = list(data.select_dtypes(exclude=[np.number]).columns)
    return non_numeric_columns


def encoding_data (data, non_numeric_columns):
    label_encoders = {}
    # Store original data before encoding
    original_data = data.copy()

    # Fit and transform each column with its respective LabelEncoder
    for col in non_numeric_columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    return data

    
def discover_casual_stracture(data):
    sm_discovered = from_pandas(data)
    return sm_discovered


def create_stracture_from_suggested_edges(suggested_edges):
    suggested_sm = StructureModel()
    suggested_sm.add_edges_from(suggested_edges)
    return suggested_sm


def saving_stracture_as_pickle(sm, name):

    with open(f'{name}.pkl', 'wb') as file:
        pickle.dump(sm, file)



def importing_stracture(data_path):   
    # Load the structure model from the file
    with open(data_path, 'rb') as file:
        sm_loaded = pickle.load(file)
        return sm_loaded


def plot_stracture(sm, data_path):
    
    viz = plot_structure(
        sm,
        all_node_attributes=NODE_STYLE.WEAK,
        all_edge_attributes=EDGE_STYLE.WEAK,
    )

    viz.toggle_physics(False)
    return viz.show(data_path)

def remove_edge_below_threshold (sm, data_path):
    sm.remove_edges_below_threshold(0.8)
    viz = plot_structure(
        sm,
        all_node_attributes=NODE_STYLE.WEAK,
        all_edge_attributes=EDGE_STYLE.WEAK,
    )
    return viz.show(data_path)