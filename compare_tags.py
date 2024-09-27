import pytest
import xml.etree.ElementTree as ET
import numpy as np
from pytest_bdd import scenarios, given, when, then

# Load feature file
scenarios('compare_tags.feature')

def extract_values_from_xml(xml_file, tag_paths):
    """
    Extracts all the float values from multiple specified nested tag paths in the XML structure.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    values_dict = {}
    
    # Iterate over each tag path and extract the corresponding values
    for tag_path in tag_paths:
        values = []
        for elem in root.findall(tag_path):
            try:
                values.append(float(elem.text))
            except ValueError:
                raise ValueError("Could not convert value {} to float".format(elem.text))
        
        values_dict[tag_path] = values
    
    return values_dict

def calculate_deltas(values_dict1, values_dict2):
    """
    Calculates the delta between two dictionaries of tag values.
    """
    deltas_dict = {}
    
    for tag_path in values_dict1:
        if tag_path not in values_dict2:
            raise ValueError("Tag path {} not found in both XMLs".format(tag_path))
        
        values1 = values_dict1[tag_path]
        values2 = values_dict2[tag_path]
        
        if len(values1) != len(values2):
            raise ValueError("The lists of values for tag {} must have the same length".format(tag_path))
        
        deltas = [v1 - v2 for v1, v2 in zip(values1, values2)]
        deltas_dict[tag_path] = deltas
    
    return deltas_dict

def standard_deviation_analysis(deltas, num_std_devs=2):
    """
    Analyzes the deltas using standard deviation and flags potential failures.
    """
    mean_delta = np.mean(deltas)
    std_dev = np.std(deltas)
    
    # Define the thresholds
    upper_threshold = mean_delta + num_std_devs * std_dev
    lower_threshold = mean_delta - num_std_devs * std_dev
    
    # Check if any deltas exceed the thresholds
    exceeding_deltas = [delta for delta in deltas if delta > upper_threshold or delta < lower_threshold]
    
    return len(exceeding_deltas), exceeding_deltas

@given('a reference XML file "<reference_file>"')
def reference_file(reference_file):
    return reference_file

@given('a test XML file "<test_file>"')
def test_file(test_file):
    return test_file

@when('I extract the values for tags "<tag_paths>"')
def extract_values(reference_file, test_file, tag_paths):
    # Convert the tag_paths string into a list (e.g., "a/b/c/d,a/b/c/e" -> ["a/b/c/d", "a/b/c/e"])
    tag_paths_list = [tag.strip() for tag in tag_paths.split(',')]
    
    # Extract values for both XML files
    reference_values_dict = extract_values_from_xml(reference_file, tag_paths_list)
    test_values_dict = extract_values_from_xml(test_file, tag_paths_list)
    
    return reference_values_dict, test_values_dict

@then('the test should pass if all deltas are within 2 standard deviations')
def compare_values(extract_values):
    reference_values_dict, test_values_dict = extract_values
    
    # Calculate deltas for all tag paths
    deltas_dict = calculate_deltas(reference_values_dict, test_values_dict)
    
    # Check each tag path for deltas exceeding the standard deviation threshold
    all_within_threshold = True
    for tag_path, deltas in deltas_dict.items():
        exceeding_count, exceeding_deltas = standard_deviation_analysis(deltas, num_std_devs=2)
        
        if exceeding_count > 0:
            all_within_threshold = False
            print("Tag path {} has {} deltas exceeding 2 standard deviations: {}".format(
                tag_path, exceeding_count, exceeding_deltas))
    
    # Assert that all deltas are within the threshold
    assert all_within_threshold, "Some deltas exceeded the threshold."
