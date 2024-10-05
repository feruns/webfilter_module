import xml.etree.ElementTree as ET
from collections import defaultdict

def print_tree(element, level=0, element_counts=None):
    indent = '  ' * level  # Indentation for tree levels
    print "%s%s (%d)" % (indent, element.tag, element_counts[element.tag])
    
    # Recursively print child elements
    for child in element:
        print_tree(child, level + 1, element_counts)

def count_elements(root):
    element_counts = defaultdict(int)
    
    # Traverse the XML tree and count each element
    for elem in root.iter():
        element_counts[elem.tag] += 1
    
    return element_counts

def parse_and_print_xml_tree(file_path):
    tree = ET.parse(file_path)  # Parse XML file
    root = tree.getroot()  # Get the root element

    element_counts = count_elements(root)  # Count elements
    print_tree(root, 0, element_counts)  # Print tree with counts

# Example usage
if __name__ == "__main__":
    xml_file_path = "example.xml"  # Replace with your XML file path
    parse_and_print_xml_tree(xml_file_path)
