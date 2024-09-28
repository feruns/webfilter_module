import xml.etree.ElementTree as ET

def extract_values_from_xml(xml_file, xpaths):
    """
    Extracts all the float values from multiple specified nested tag paths in the XML structure.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    values_dict = {}
    
    for xpath in xpaths:
        values = []
        for elem in root.findall(xpath):
            try:
                values.append(float(elem.text))
            except ValueError:
                raise ValueError("Could not convert value {} to float".format(elem.text))
        
        values_dict[xpath] = values
    
    return values_dict

def calculate_deltas(values_dict1, values_dict2):
    """
    Calculates the delta between two dictionaries of tag values.
    """
    deltas_dict = {}
    
    for xpath in values_dict1:
        if xpath not in values_dict2:
            raise ValueError("Tag path {} not found in both XMLs".format(xpath))
        
        values1 = values_dict1[xpath]
        values2 = values_dict2[xpath]
        
        if len(values1) != len(values2):
            raise ValueError("The lists of values for tag {} must have the same length".format(xpath))
        
        deltas = [v1 - v2 for v1, v2 in zip(values1, values2)]
        deltas_dict[xpath] = deltas
    
    return deltas_dict

def compare_xml_files_with_tolerance(reference_file, test_file, xpaths_tolerance_list):
    """
    Compare two XML files based on xpaths and tolerances.
    Returns True if all deltas are within tolerance, otherwise raises an AssertionError.
    """
    xpaths = [xpath for xpath, _ in xpaths_tolerance_list]
    
    # Extract values from XML files
    reference_values_dict = extract_values_from_xml(reference_file, xpaths)
    test_values_dict = extract_values_from_xml(test_file, xpaths)
    
    # Calculate deltas for all xpaths
    deltas_dict = calculate_deltas(reference_values_dict, test_values_dict)
    
    # Check each xpath for deltas exceeding the specified tolerance
    for xpath, tolerance in xpaths_tolerance_list:
        deltas = deltas_dict[xpath]
        
        exceeding_deltas = [delta for delta in deltas if abs(delta) > tolerance]
        
        if exceeding_deltas:
            raise AssertionError(f"XPath {xpath} has {len(exceeding_deltas)} deltas exceeding tolerance {tolerance}: {exceeding_deltas}")
    
    return True
