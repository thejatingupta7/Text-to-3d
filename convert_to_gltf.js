import fs from 'fs';
import path from 'path';

async function convertToGLTF(sceneCode, outputPath) {
    try {
        // Import Three.js modules dynamically
        const { GLTFExporter } = await import('three/examples/jsm/exporters/GLTFExporter.js');
        const { ObjectLoader } = await import('three');
        const THREE = await import('three');

        // Create a temporary file with the scene code
        const tempFile = path.join(__dirname, 'temp_scene.js');
        fs.writeFileSync(tempFile, sceneCode);

        // Create a new scene
        const scene = new THREE.Scene();
        
        // Execute the scene code in a safe context
        const createScene = new Function('THREE', sceneCode);
        const sceneGroup = createScene(THREE);
        scene.add(sceneGroup);

        // Export to GLTF
        const exporter = new GLTFExporter();
        const gltf = await new Promise((resolve, reject) => {
            exporter.parse(scene, (gltf) => resolve(gltf), { binary: false }, (error) => reject(error));
        });

        // Save the GLTF file
        fs.writeFileSync(outputPath, JSON.stringify(gltf, null, 2));
        
        // Clean up
        fs.unlinkSync(tempFile);
        
        return true;
    } catch (error) {
        console.error('Error converting to GLTF:', error);
        return false;
    }
}

export { convertToGLTF }; 