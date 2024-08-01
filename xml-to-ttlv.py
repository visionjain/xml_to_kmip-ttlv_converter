from flask import Flask, request, render_template
import struct
import xml.etree.ElementTree as ET
import binascii

app = Flask(__name__)

tag_map = {
    "RequestMessage":      0x420078,
    "RequestHeader":       0x420077,
    "ProtocolVersion":     0x420069,
    "ProtocolVersionMajor": 0x42006A,
    "ProtocolVersionMinor": 0x42006B,
    "BatchCount":          0x42000D,
    "BatchItem":           0x42000F,
    "Operation":           0x42005C,
    "RequestPayload":      0x420079,
    "ObjectType":          0x420057,
    "TemplateAttribute":   0x420091,
    "Attribute":           0x420008,
    "AttributeName":       0x42000A,
    "AttributeValue":      0x42000B,
}

type_map = {
    "Structure":    0x01,
    "Integer":      0x02,
    "Long Integer": 0x03,
    "Big Integer":  0x04,
    "Enumeration":  0x05,
    "Boolean":      0x06,
    "TextString":   0x07,
    "ByteString":   0x08,
    "Date-Time":    0x09,
    "Interval":     0x0A,
}

enum_map = {
    "Create":        0x01,
    "SymmetricKey":  0x02,
    "AES":           0x03,
}

def encode_tag(tag):
    tag_bytes = struct.pack(">I", tag)
    return tag_bytes[1:]

def encode_type(type_str):
    return type_map[type_str]

def encode_length(length):
    return struct.pack(">I", length)

def encode_value(value, type_str):
    if type_str == "Integer":
        encoded_value = struct.pack(">I", int(value))
        length = 4
    elif type_str == "Long Integer":
        encoded_value = struct.pack(">Q", int(value))
        length = 8
    elif type_str == "Big Integer":
        encoded_value = int(value).to_bytes((int(value).bit_length() + 7) // 8, byteorder='big')
        length = len(encoded_value)
    elif type_str == "Enumeration":
        encoded_value = struct.pack(">I", enum_map[value])
        length = 4
    elif type_str == "Boolean":
        encoded_value = struct.pack(">Q", 1 if value.lower() == "true" else 0)
        length = 8
    elif type_str == "TextString":
        encoded_value = value.encode()
        length = len(encoded_value)
    elif type_str == "ByteString":
        encoded_value = binascii.unhexlify(value)
        length = len(encoded_value)
    elif type_str == "Date-Time":
        encoded_value = struct.pack(">Q", int(value))
        length = 8
    elif type_str == "Interval":
        encoded_value = struct.pack(">I", int(value))
        length = 4
    else:
        raise ValueError(f"Unsupported type: {type_str}")

    padding_length = (8 - length % 8) % 8
    return encoded_value + b'\x00' * padding_length, length

def ttlv_encode(tag, type_str, value, length):
    encoded_tag = encode_tag(tag)
    encoded_type = encode_type(type_str)
    encoded_length = encode_length(length)

    return encoded_tag + bytes([encoded_type]) + encoded_length + value

def parse_element(element):
    tag = tag_map[element.tag]
    type_str = element.attrib.get('type', '')

    if type_str == "" and len(element):
        type_str = "Structure"

    if type_str == "Structure":
        sub_elements = b''
        for sub_element in element:
            sub_elements += parse_element(sub_element)
        return ttlv_encode(tag, "Structure", sub_elements, len(sub_elements))
    else:
        value, length = encode_value(element.attrib['value'], type_str)
        return ttlv_encode(tag, type_str, value, length)

def xml_to_ttlv(xml_str):
    root = ET.fromstring(xml_str)
    ttlv_elements = parse_element(root)
    return binascii.hexlify(ttlv_elements).upper().decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    xml_input = '''<RequestMessage>
        <RequestHeader>
            <ProtocolVersion>
                <ProtocolVersionMajor type="Integer" value="1"/>
                <ProtocolVersionMinor type="Integer" value="0"/>
            </ProtocolVersion>
            <BatchCount type="Integer" value="1"/>
        </RequestHeader>
        <BatchItem>
            <Operation type="Enumeration" value="Create"/>
            <RequestPayload>
                <ObjectType type="Enumeration" value="SymmetricKey"/>
                <TemplateAttribute>
                    <Attribute>
                        <AttributeName type="TextString" value="Cryptographic Algorithm"/>
                        <AttributeValue type="Enumeration" value="AES"/>
                    </Attribute>
                    <Attribute>
                        <AttributeName type="TextString" value="Cryptographic Length"/>
                        <AttributeValue type="Integer" value="128"/>
                    </Attribute>
                    <Attribute>
                        <AttributeName type="TextString" value="Cryptographic Usage Mask"/>
                        <AttributeValue type="Integer" value="12"/>
                    </Attribute>
                </TemplateAttribute>
            </RequestPayload>
        </BatchItem>
    </RequestMessage>'''

    ttlv_output = ''
    if request.method == 'POST':
        xml_input = request.form['xml_input']
        ttlv_output = xml_to_ttlv(xml_input)

    return render_template('index.html', xml_input=xml_input, ttlv_output=ttlv_output)

if __name__ == "__main__":
    app.run(debug=True)
