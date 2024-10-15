import os
import sys
import pandas as pd
from faker import Faker
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

@dataclass
class SyntheticDataGenerationConfig:
    raw_data_path: str = os.path.join('raw_data', 'data.csv')
    synthetic_data_file_path: str = os.path.join('synthetic_data', 'synthetic_data.csv')

class SyntheticDataGenerator:
    
    def __init__(self, num_initial_rows=1000, num_synthetic_rows=10000):
        self.num_initial_rows = num_initial_rows
        self.num_synthetic_rows = num_synthetic_rows
        self.fake = Faker()
        self.synthetic_data_config = SyntheticDataGenerationConfig()

    def generate_row(self):
        return {
            'RowNumber': self.fake.random_int(min=1, max=1000000),
            'CustomerId': self.fake.uuid4(),
            'Surname': self.fake.last_name(),
            'CreditScore': self.fake.random_int(min=300, max=900),
            'Geography': self.fake.random_element(elements=('France', 'Spain', 'Germany')),
            'Gender': self.fake.random_element(elements=('Male', 'Female')),
            'Age': self.fake.random_int(min=18, max=95),
            'Tenure': self.fake.random_int(min=0, max=10),
            'Balance': round(self.fake.random.uniform(0.0, 260898.09), 2),
            'NumOfProducts': self.fake.random_int(min=1, max=4),
            'HasCrCard': self.fake.random_int(min=0, max=1),
            'IsActiveMember': self.fake.random_int(min=0, max=1),
            'EstimatedSalary': round(self.fake.random.uniform(10.58, 199998.88), 2),
            'Exited': self.fake.random_int(min=0, max=1)
        }

    def generate_initial_data(self):
        try:
            initial_data = [self.generate_row() for _ in range(self.num_initial_rows)]
            df = pd.DataFrame(initial_data)
            
            os.makedirs(os.path.dirname(self.synthetic_data_config.raw_data_path), exist_ok=True)
            df.to_csv(self.synthetic_data_config.raw_data_path, index=False)
            
            logging.info(f"Initial data generated and saved to {self.synthetic_data_config.raw_data_path}")
            return self.synthetic_data_config.raw_data_path
        except Exception as e:
            raise CustomException(e, sys)

    def generate_synthetic_data(self):
        try:
            if not os.path.exists(self.synthetic_data_config.raw_data_path):
                self.generate_initial_data()
            
            df = pd.read_csv(self.synthetic_data_config.raw_data_path)
            
            new_rows = [self.generate_row() for _ in range(self.num_synthetic_rows)]
            new_df = pd.DataFrame(new_rows)
            synthetic_data = pd.concat([df, new_df], ignore_index=True)
            
            os.makedirs(os.path.dirname(self.synthetic_data_config.synthetic_data_file_path), exist_ok=True)
            synthetic_data.to_csv(self.synthetic_data_config.synthetic_data_file_path, index=False)
        
            logging.info(f"Synthetic data generated and saved to {self.synthetic_data_config.synthetic_data_file_path}")
            return self.synthetic_data_config.synthetic_data_file_path
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":       
    gen_df = SyntheticDataGenerator()
    synthetic_data_path = gen_df.generate_synthetic_data()
    print(f"Synthetic data generated and saved to {synthetic_data_path}")
