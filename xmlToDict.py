import xml.etree.ElementTree as ET

def xml_to_dict(element):
    # Ensure the element's tag is in byte string format (str in Python 2)
    tag = element.tag.encode('utf-8') if isinstance(element.tag, unicode) else element.tag
    node_dict = {tag: []}
    
    # Process each child of the element
    for child in element:
        child_tag = child.tag.encode('utf-8') if isinstance(child.tag, unicode) else child.tag
        if len(child) > 0:
            node_dict[tag].append(xml_to_dict(child))
        else:
            # If the child has no children, encode its text content as needed
            text = child.text.encode('utf-8') if isinstance(child.text, unicode) else child.text
            node_dict[tag].append({child_tag: text})
    
    return node_dict

def parse_xml_to_nested_dict(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Convert the root element to a nested dictionary
    return xml_to_dict(root)

# Example usage
if __name__ == "__main__":
    xml_file_path = "example.xml"  # Replace with your XML file path
    nested_dict = parse_xml_to_nested_dict(xml_file_path)
    print(nested_dict)
