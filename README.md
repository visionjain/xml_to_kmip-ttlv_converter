
# XML to KMIP TTLV Converter

This project provides a web interface for converting XML to KMIP TTLV format using Flask. The interface includes an input box for XML, a button to perform the conversion, and an output box to display the TTLV representation.

## Prerequisites

- Python 3.x
- Flask

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/visionjain/xml_to_kmip-ttlv_converter
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```sh
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

4. **Install Flask**

   ```sh
   pip install Flask
   ```

## Usage

1. **Run the Flask Application**

   ```sh
   python xml-to-ttlv.py
   ```

2. **Open in Browser**

   Open your web browser and go to `http://127.0.0.1:5000/`. You should see the web interface for converting XML to KMIP TTLV format. Enter your XML in the provided box and click the "Convert" button to see the TTLV output.

## Directory Structure

```
xml-to-kmip-ttlv-converter/
│
├── xml-to-ttlv.py
└── templates/
    └── index.html
```

## HTML Template

Make sure to place the `index.html` file inside the `templates` directory.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
