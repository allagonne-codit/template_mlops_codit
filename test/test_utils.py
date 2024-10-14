import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mlops-best-practices')))

import pandas as pd
from collections import Counter
import pytest
from src.utils import fix_outliers, class_imbalance, handling_class_imbalance
from src.exception import CustomException

def test_fix_outliers():
    data = pd.Series([1, 2, 3, 4, 100])
    expected_output = pd.Series([1, 2, 3, 4, 4])  # Assuming Q3 is 4
    result = fix_outliers(data)
    pd.testing.assert_series_equal(result, expected_output)

def test_class_imbalance():
    y_train = [0, 0, 0, 1]
    thresh = 50  # 50% imbalance threshold
    result = class_imbalance(y_train, thresh)
    assert result == True

def test_handling_class_imbalance():
    X = pd.DataFrame({'feature1': [1, 2, 3, 4], 'feature2': [5, 6, 7, 8]})
    y = [0, 0, 0, 1]
    thresh = 50  # 50% imbalance threshold
    result = handling_class_imbalance(X, y, thresh)
    assert result is not None  # Assuming the function returns some value