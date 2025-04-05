# 3D Scene Generator

A web application that allows users to generate 3D scenes and models from text descriptions using AI technologies.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a09ecc96-4a60-4fe3-b1c7-614531fb2861" width="200"/>
  <img src="https://github.com/user-attachments/assets/28a5ef55-ad95-48d9-a0a4-24d9ee69411f" width="200"/>
  <img src="https://github.com/user-attachments/assets/245b76bd-bee4-4bed-b9e9-6e593d76bd0b" width="200"/>
  <img src="https://github.com/user-attachments/assets/f8d1bf1c-b775-408d-9819-f21168360038" width="200"/>
</p>


---


## Features

- Generate Three.js-compatible 3D scenes from text prompts
- Create realistic 3D models using Tripo3D API integration
- Interactive 3D viewport using Three.js
- Download 3D models in glTF/GLB format
- Modern, responsive web interface

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **3D Rendering**: Three.js
- **AI Services**:
  - Azure OpenAI API for scene generation
  - Tripo3D API for 3D model creation

## Setup Instructions

### Prerequisites

- Python 3.6+
- Node.js (for optional tools)

### Installation

1. Clone the repository
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` file:
   ```
   OPENAI_API_KEY=your_api_key
   TRIPO3D_API_KEY=your_tripo3d_api_key
   ```

### Running the Application

1. Start the Flask server:
   ```
   python server.py
   ```
2. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Enter a descriptive prompt for the 3D scene or model you want to generate
2. Click "Generate Scene" to create a Three.js scene
3. Click "Generate 3D Model" to create a detailed 3D model using Tripo3D
4. View and interact with the 3D result in the viewport
5. Download the generated model if desired

## Project Structure

- `server.py`: Main Flask application with API endpoints
- `templates/index.html`: Frontend interface
- `static/`: Directory for static assets
  - `scenes/`: Generated Three.js scene files
  - `models/`: Generated 3D models
- `convert_to_gltf.js`: Utility for format conversion

## License

[Apache 2.0 License](LICENSE) 
