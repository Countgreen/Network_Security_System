from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTrasnformationConfig,ModelTrainerConfig
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
        data_transformation_config=DataTrasnformationConfig(Training_Pipeline_Config)
        logging.info("Data Transformation Started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation Completed")
        logging.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfig(Training_Pipeline_Config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)



