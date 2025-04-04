Creating a full-featured cat model in Three.js is a complex task involving detailed geometry and textures. For simplicity, I'll create a cartoonish, blocky representation of a cat using basic shapes.

```javascript
function createScene() {
    const scene = new THREE.Group();

    // Cat body
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(2, 1, 1),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    body.position.set(0, 0.5, 0);
    scene.add(body);

    // Cat head
    const head = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    head.position.set(0, 1.25, 0);
    scene.add(head);

    // Left ear
    const leftEar = new THREE.Mesh(
        new THREE.ConeGeometry(0.3, 0.5, 4),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    leftEar.position.set(-0.35, 1.8, 0);
    leftEar.rotation.set(0, 0, Math.PI / 4); // Rotate to make it upright
    scene.add(leftEar);

    // Right ear
    const rightEar = new THREE.Mesh(
        new THREE.ConeGeometry(0.3, 0.5, 4),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    rightEar.position.set(0.35, 1.8, 0);
    rightEar.rotation.set(0, 0, -Math.PI / 4); // Rotate to make it upright
    scene.add(rightEar);

    // Tail
    const tail = new THREE.Mesh(
        new THREE.CylinderGeometry(0.1, 0.1, 1.5, 8),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    tail.position.set(0, 0.5, -0.6);
    tail.rotation.set(Math.PI / 4, 0, 0); // Angle the tail upwards
    scene.add(tail);

    // Left front leg
    const leftFrontLeg = new THREE.Mesh(
        new THREE.CylinderGeometry(0.1, 0.1, 0.6, 8),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    leftFrontLeg.position.set(-0.5, 0.3, 0.3);
    scene.add(leftFrontLeg);

    // Right front leg
    const rightFrontLeg = new THREE.Mesh(
        new THREE.CylinderGeometry(0.1, 0.1, 0.6, 8),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    rightFrontLeg.position.set(0.5, 0.3, 0.3);
    scene.add(rightFrontLeg);

    // Left back leg
    const leftBackLeg = new THREE.Mesh(
        new THREE.CylinderGeometry(0.1, 0.1, 0.6, 8),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    leftBackLeg.position.set(-0.5, 0.3, -0.3);
    scene.add(leftBackLeg);

    // Right back leg
    const rightBackLeg = new THREE.Mesh(
        new THREE.CylinderGeometry(0.1, 0.1, 0.6, 8),
        new THREE.MeshStandardMaterial({ color: 0x808080 }) // Gray color
    );
    rightBackLeg.position.set(0.5, 0.3, -0.3);
    scene.add(rightBackLeg);

    // Add eyes
    const leftEye = new THREE.Mesh(
        new THREE.SphereGeometry(0.1, 16, 16),
        new THREE.MeshStandardMaterial({ color: 0x000000 }) // Black
    );
    leftEye.position.set(-0.25, 1.3, 0.5);
    scene.add(leftEye);

    const rightEye = new THREE.Mesh(
        new THREE.SphereGeometry(0.1, 16, 16),
        new THREE.MeshStandardMaterial({ color: 0x000000 }) // Black
    );
    rightEye.position.set(0.25, 1.3, 0.5);
    scene.add