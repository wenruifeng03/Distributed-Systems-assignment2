from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import os
import requests

XML_DB = "C:/Users/86188/Desktop/project/notebook.xml"

def init_xml_db():
    if not os.path.exists(XML_DB):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(XML_DB)

def add_note(topic, notename, text, timestamp):
    try:
        tree = ET.parse(XML_DB)
    except ET.ParseError:
        init_xml_db()
        tree = ET.parse(XML_DB)

    root = tree.getroot()
    if root is None:
        root = ET.Element("data")
        tree = ET.ElementTree(root)
    
    
    topic_elem = None
    for t in root.findall("topic"):
        if t.attrib.get("name") == topic:
            topic_elem = t
            break
    if topic_elem is None:
        topic_elem = ET.SubElement(root, "topic", name=topic)
    
    note_elem = ET.SubElement(topic_elem, "note", name=notename)

    text_elem = ET.SubElement(note_elem, "text")
    text_elem.text = text
    
    timestamp_elem = ET.SubElement(note_elem, "timestamp")
    timestamp_elem.text = timestamp
    
    tree.write(XML_DB)
    return True

def get_notes(topic):
    tree = ET.parse(XML_DB)
    root = tree.getroot()
    for t in root.findall("topic"):
        if t.attrib.get("name") == topic:
            notes = []
            for note in t.findall("note"):
                text_elem = note.find("text")
                timestamp_elem = note.find("timestamp")
                note_text = text_elem.text if text_elem is not None else ""
                note_timestamp = timestamp_elem.text if timestamp_elem is not None else ""
                notes.append({
                    "notename": note.attrib.get("name", ""),
                    "timestamp": note_timestamp,
                    "text": note_text
                })
            return notes
    return []

def query_wiki(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": topic,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if len(data) >= 4 and data[3]:
        return data[3][0]
    else:
        return "No found."

if __name__ == "__main__":
    init_xml_db()
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    print("The server starts, listening on port 8000...")
    server.register_function(add_note, "add_note")
    server.register_function(get_notes, "get_notes")
    server.register_function(query_wiki, "query_wiki")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("The server is shut down.")
