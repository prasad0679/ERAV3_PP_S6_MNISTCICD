import json
import pytest

def test_model_metrics():
    with open('model_metrics.json', 'r') as f:
        metrics = json.load(f)
    
    # Test number of parameters
    assert metrics['total_parameters'] < 20000, "Model parameters exceed 20,000"
    
    # Test number of epochs
    assert metrics['best_epoch'] < 20, "Number of epochs exceeds 20"
    
    # Test accuracy
    assert metrics['test_accuracy'] >= 99.4, "Test accuracy is less than 99.4%" 