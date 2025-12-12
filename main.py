from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        Training_Pipeline_Config=TrainingPipelineConfig()
        Data_Ingestion_Config=DataIngestionConfig(TrainingPipelineConfig)
        Data_Ingestion=DataIngestion(Data_Ingestion_Config)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=Data_Ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(Training_Pipeline_Config)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



