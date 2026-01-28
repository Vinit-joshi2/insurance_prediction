import sys
import os
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder , OrdinalEncoder , LabelEncoder

from sklearn.compose import ColumnTransformer

from src.constants import TARGET_COLUMN , SCHEMA_FILE_PATH , CURRENT_YEAR
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact , DataIngestionArtifact , DataValidationArtifact
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_numpy_array_data , save_object , read_yaml_file





class DataTransformations:

    def __init__(self , data_ingestion_artifact :DataIngestionArtifact , 
                 data_transformation_config:DataTransformationArtifact ,
                 data_validation_artifact:DataValidationArtifact
                 ):
        

        try:
            self.data_ingestion_artifact = data_ingestion_artifact , 
            self.data_transformation_artifact = data_transformation_config
            self.data_validation_config = data_validation_artifact

        except Exception as e:
            raise MyException(e,sys)