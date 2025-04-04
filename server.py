import os
from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from openai import OpenAI
import time
import re
import json
import subprocess
import tempfile
import requests  # Add requests library for Tripo3D API

# Initialize Flask app
app = Flask(__name__)

# Create directory for generated scenes if it doesn't exist
SCENES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'scenes')
os.makedirs(SCENES_DIR, exist_ok=True)

# Create directory for 3D models if it doesn't exist
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Setup Azure OpenAI API
token = "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"
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Tripo3D API settings
TRIPO3D_API_KEY = "tsk_1LlF24J8qJIebtlxpyJ_1yFYD67eHLzZHOteXPkdC6h"  # Replace with your actual API key
TRIPO3D_API_URL = "https://api.tripo3d.ai/v2/openapi/task"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scenes/<path:filename>")
def serve_scene(filename):
    return send_from_directory(SCENES_DIR, filename)

@app.route("/models/<path:filename>")
def serve_model(filename):
    return send_from_directory(MODELS_DIR, filename)

@app.route("/generate_3d", methods=["POST"])
def generate_3d():
    user_input = request.json.get("prompt", "")
    
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Call Azure OpenAI API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a 3D scene generation assistant. Convert user descriptions into Three.js compatible scene descriptions.
                    Return the response in the following format:
                    ```javascript
                    function createScene() {
                        const scene = new THREE.Group();
                        
                        // Add objects here
                        const box = new THREE.Mesh(
                            new THREE.BoxGeometry(1, 1, 1),
                            new THREE.MeshStandardMaterial({ color: 0x00ff00 })
                        );
                        scene.add(box);
                        
                        return scene;
                    }
                    ```"""
                },
                {
                    "role": "user",
                    "content": f"Generate a Three.js scene based on this description: {user_input}"
                }
            ],
            temperature=0.7,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        
        # Get the raw content from the response
        raw_content = response.choices[0].message.content
        
        # Try to extract the code block
        code_match = re.search(r"```javascript\s*([\s\S]*?)\s*```", raw_content)
        
        if not code_match:
            # If no code block found, try to find any code block
            code_match = re.search(r"```\s*([\s\S]*?)\s*```", raw_content)
            
        if not code_match:
            # If still no match, use the entire content
            generated_content = raw_content
        else:
            generated_content = code_match.group(1).strip()

        # Generate a unique filename based on timestamp
        timestamp = int(time.time())
        scene_filename = "current_scene.js"
        scene_path = os.path.join(SCENES_DIR, scene_filename)

        # Save the generated Three.js code to a file
        with open(scene_path, 'w') as f:
            f.write(generated_content)

        # Return success status
        return jsonify({
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print error to console
        return jsonify({"error": str(e)}), 500

@app.route("/generate_tripo3d_model", methods=["POST"])
def generate_tripo3d_model():
    user_input = request.json.get("prompt", "")
    
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Define headers for Tripo3D API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TRIPO3D_API_KEY}"
        }
        
        # Define the data payload
        data = {
            "type": "text_to_model",
            "prompt": user_input,
            "model_version": "v2.5-20250123"  # Using the specified model version
        }
        
        # Log the request
        print(f"Sending request to Tripo3D API: {json.dumps(data)}")
        
        # Make the POST request to Tripo3D API
        response = requests.post(TRIPO3D_API_URL, headers=headers, json=data)
        
        # Log the full response for debugging
        print(f"Tripo3D API response: {response.text}")
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Check all possible locations for task_id
            task_id = None
            
            # Try to find task_id in different possible locations
            if "data" in response_data:
                data_obj = response_data.get("data", {})
                
                # Check direct task_id field
                if "task_id" in data_obj:
                    task_id = data_obj.get("task_id")
                # Check id field (some APIs use id instead of task_id)
                elif "id" in data_obj:
                    task_id = data_obj.get("id")
            
            # If we still don't have a task_id, check at the top level
            if task_id is None:
                task_id = response_data.get("task_id") or response_data.get("id")
                
            print(f"Extracted task_id: {task_id}")
            
            if task_id:
                return jsonify({
                    "status": "success",
                    "task_id": task_id
                })
            else:
                print("No task ID found in response structure:", response_data)
                return jsonify({"error": "No task ID returned from Tripo3D API"}), 500
        else:
            return jsonify({"error": f"Tripo3D API error: {response.text}"}), response.status_code
        
    except Exception as e:
        print(f"Error occurred with Tripo3D API: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/check_tripo3d_status/<task_id>", methods=["GET"])
def check_tripo3d_status(task_id):
    try:
        # Define headers for Tripo3D API
        headers = {
            "Authorization": f"Bearer {TRIPO3D_API_KEY}"
        }
        
        # Create the status URL
        status_url = f"https://api.tripo3d.ai/v2/openapi/task/{task_id}"
        
        # Make the GET request to check status
        status_response = requests.get(status_url, headers=headers)
        
        # Print the full response for debugging
        print(f"Status response for task {task_id}: {status_response.text}")
        
        # Check if the request was successful
        if status_response.status_code == 200:
            status_data = status_response.json()
            
            # Extract task status, printing the full data structure for debugging
            print(f"Status data: {json.dumps(status_data, indent=2)}")
            
            # Get the status from the appropriate place in the response
            if "data" in status_data and status_data["data"]:
                data = status_data["data"]
                
                # Check if the status is success
                if data.get("status") == "success":
                    # Extract preview image URL from rendered_image section
                    preview_image_url = None
                    if "result" in data and "rendered_image" in data["result"] and "url" in data["result"]["rendered_image"]:
                        preview_image_url = data["result"]["rendered_image"]["url"]
                    
                    # Look for the download URL in the result.pbr_model.url path
                    if "result" in data and "pbr_model" in data["result"] and "url" in data["result"]["pbr_model"]:
                        download_url = data["result"]["pbr_model"]["url"]
                        
                        # Download the model
                        model_response = requests.get(download_url)
                        
                        if model_response.status_code == 200:
                            # Save the model file locally with a timestamp
                            timestamp = int(time.time())
                            model_filename = f"tripo3d_model_{timestamp}.glb"
                            model_path = os.path.join(MODELS_DIR, model_filename)
                            
                            with open(model_path, "wb") as file:
                                file.write(model_response.content)
                            
                            # If preview image is available, download it too
                            preview_path = None
                            if preview_image_url:
                                try:
                                    preview_response = requests.get(preview_image_url)
                                    if preview_response.status_code == 200:
                                        preview_filename = f"preview_{timestamp}.webp"
                                        preview_path = os.path.join(MODELS_DIR, preview_filename)
                                        with open(preview_path, "wb") as file:
                                            file.write(preview_response.content)
                                        preview_path = f"/models/{preview_filename}"
                                except Exception as img_err:
                                    print(f"Error downloading preview image: {str(img_err)}")
                            
                            response_data = {
                                "status": "completed",
                                "model_path": f"/models/{model_filename}"
                            }
                            
                            # Add preview image path if available
                            if preview_path:
                                response_data["preview_image"] = preview_path
                            
                            return jsonify(response_data)
                        else:
                            return jsonify({"error": f"Failed to download model file: {model_response.status_code} - {model_response.text}"}), 500
                    else:
                        return jsonify({"error": "Model completed but could not find download URL in the response structure"}), 500
                else:
                    # Task still in progress, processing, or other status
                    return jsonify({
                        "status": data.get("status") or "unknown"
                    })
            else:
                # No data field found
                return jsonify({
                    "status": "unknown",
                    "error": "Invalid response format from Tripo3D API"
                })
        else:
            return jsonify({"error": f"Error checking task status: {status_response.text}"}), status_response.status_code
        
    except Exception as e:
        print(f"Error checking Tripo3D status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/download_gltf")
def download_gltf():
    try:
        # Read the current scene file
        scene_path = os.path.join(SCENES_DIR, 'current_scene.js')
        if not os.path.exists(scene_path):
            return jsonify({"error": "No scene file found"}), 404

        with open(scene_path, 'r') as f:
            scene_code = f.read()

        # Create a temporary GLTF file
        gltf_path = os.path.join(SCENES_DIR, 'model.gltf')
        
        # Run the Node.js conversion script
        result = subprocess.run([
            'node',
            'convert_to_gltf.js',
            scene_path,
            gltf_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Conversion failed: {result.stderr}")

        # Send the GLTF file
        return send_file(
            gltf_path,
            mimetype='model/gltf+json',
            as_attachment=True,
            download_name='model.gltf'
        )

    except Exception as e:
        print(f"Error generating GLTF: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5001, host='0.0.0.0')
    except Exception as e:
        print(f"Failed to start server: {str(e)}")
