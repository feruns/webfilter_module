from robot.api import logger

def compare_xml_files_with_tolerance(reference_file, test_file, xpaths_tolerance_string):
    """
    Compare two XML files based on XPaths and tolerances.
    The XPath-tolerance pairs are passed as a multi-line string with each pair on a new line.
    """
    # Convert the string into a dictionary
    xpaths_tolerance_dict = parse_xpaths_tolerance_string(xpaths_tolerance_string)

    # Extract values from the XML files using the XPaths
    reference_values_dict = extract_values_from_xml(reference_file, list(xpaths_tolerance_dict.keys()))
    test_values_dict = extract_values_from_xml(test_file, list(xpaths_tolerance_dict.keys()))

    # Calculate deltas for all xpaths
    deltas_dict = calculate_deltas(reference_values_dict, test_values_dict)

    # Iterate over each XPath and its corresponding tolerance
    for xpath, tolerance in xpaths_tolerance_dict.items():
        deltas = deltas_dict.get(xpath, [])

        # Find any deltas exceeding the tolerance
        exceeding_deltas = [delta for delta in deltas if abs(delta) > tolerance]

        if exceeding_deltas:
            raise AssertionError(f"XPath '{xpath}' has {len(exceeding_deltas)} deltas exceeding tolerance {tolerance}: {exceeding_deltas}")

    logger.info("XML comparison passed all tolerance checks", also_console=True)
    return True


def parse_xpaths_tolerance_string(xpaths_tolerance_string):
    """
    Convert the string of XPath-tolerance pairs into a dictionary.
    Each line of the string should be in the format: 'XPath tolerance'
    """
    xpaths_tolerance_dict = {}
    
    # Split the string into lines
    lines = xpaths_tolerance_string.strip().splitlines()
    
    # Process each line
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            xpath = parts[0]
            tolerance = float(parts[1])
            xpaths_tolerance_dict[xpath] = tolerance
        else:
            raise ValueError(f"Invalid format for line: {line}")
    
    return xpaths_tolerance_dict
