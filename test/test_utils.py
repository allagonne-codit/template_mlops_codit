import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
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
    # Test case 1: Imbalanced data
    X_imbalanced = pd.DataFrame({'feature1': [1, 2, 3, 4], 'feature2': [5, 6, 7, 8]})
    y_imbalanced = [0, 0, 0, 1]
    thresh_imbalanced = 50  # 50% imbalance threshold
    
    print(f"X_imbalanced: {X_imbalanced}")  # Debug print
    print(f"y_imbalanced: {y_imbalanced}")  # Debug print
    print(f"thresh_imbalanced: {thresh_imbalanced}")  # Debug print
    
    result_imbalanced = handling_class_imbalance(X_imbalanced, y_imbalanced, thresh_imbalanced)
    print(f"Result imbalanced: {result_imbalanced}")  # Debug print
    
    assert result_imbalanced is not None, "Result should not be None for imbalanced data"
    assert len(result_imbalanced[0]) > len(X_imbalanced), "Number of samples should increase after balancing"
    assert len(result_imbalanced[0]) == len(result_imbalanced[1]), "X and y should have the same length after balancing"

    # Test case 2: Balanced data
    X_balanced = pd.DataFrame({'feature1': [1, 2, 3, 4], 'feature2': [5, 6, 7, 8]})
    y_balanced = [0, 0, 1, 1]
    thresh_balanced = 50  # 50% imbalance threshold
    
    print(f"X_balanced: {X_balanced}")  # Debug print
    print(f"y_balanced: {y_balanced}")  # Debug print
    print(f"thresh_balanced: {thresh_balanced}")  # Debug print
    
    result_balanced = handling_class_imbalance(X_balanced, y_balanced, thresh_balanced)
    print(f"Result balanced: {result_balanced}")  # Debug print
    
    assert result_balanced is not None, "Function should return original data for already balanced data"
    assert len(result_balanced[0]) == len(X_balanced), "Number of samples should not change for balanced data"
    assert len(result_balanced[0]) == len(result_balanced[1]), "X and y should have the same length"
