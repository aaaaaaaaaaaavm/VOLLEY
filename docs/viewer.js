const el = document.getElementById('cadViewer');
if (el) {
  const status = el.querySelector('[data-viewer-status]');
  let renderer;
  let controls;
  let group;
  async function startViewer() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('webgl2', {antialias: true});
    if (!context) throw new Error('3D graphics unavailable');
    const [THREE, controlModule, loaderModule] = await Promise.all([
      import('https://esm.sh/three@0.180.0'),
      import('https://esm.sh/three@0.180.0/examples/jsm/controls/OrbitControls.js'),
      import('https://esm.sh/three@0.180.0/examples/jsm/loaders/STLLoader.js')
    ]);
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x08111e);
    const cam = new THREE.PerspectiveCamera(42, 1, .1, 10000);
    renderer = new THREE.WebGLRenderer({canvas, context, antialias: true});
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    scene.add(new THREE.HemisphereLight(0xddeeff, 0x18283b, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 3);
    key.position.set(2, 3, 4);
    scene.add(key);
    group = new THREE.Group();
    scene.add(group);
    const loader = new loaderModule.STLLoader();
    const root = 'https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/cad/stl/';
    const parts = [
      ['VOLLEY_Track_Gen5.stl', 0x8d949d],
      ['VOLLEY_Stator_Gen5.stl', 0xb8622f],
      ['VOLLEY_Sled_Gen5.stl', 0xbfc7d1],
      ['VOLLEY_Payload_3U_Gen5.stl', 0x5b8cc5]
    ];
    await Promise.all(parts.map(([file, color]) => new Promise((resolve, reject) => {
      loader.load(root + file, geometry => {
        geometry.computeVertexNormals();
        group.add(new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
          color, metalness: .35, roughness: .5
        })));
        resolve();
      }, undefined, reject);
    })));
    const box = new THREE.Box3().setFromObject(group);
    const size = box.getSize(new THREE.Vector3()).length();
    if (!Number.isFinite(size) || size <= 0) throw new Error('Empty CAD geometry');
    group.position.sub(box.getCenter(new THREE.Vector3()));
    cam.position.set(size*.65, size*.45, size*.75);
    cam.near = size/1000;
    cam.far = size*10;
    cam.updateProjectionMatrix();
    controls = new controlModule.OrbitControls(cam, renderer.domElement);
    controls.enableDamping = true;
    controls.autoRotate = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    controls.autoRotateSpeed = .7;
    controls.target.set(0, 0, 0);
    controls.update();
    function resize() {
      const w = el.clientWidth, h = Math.max(360, Math.min(620, w*.58));
      renderer.setSize(w, h, false);
      cam.aspect = w/h;
      cam.updateProjectionMatrix();
    }
    resize();
    renderer.render(scene, cam);
    // Replace the useful static view only after all geometry renders successfully.
    el.replaceChildren(renderer.domElement);
    el.classList.remove('static');
    addEventListener('resize', resize);
    function loop() {
      requestAnimationFrame(loop);
      controls.update();
      renderer.render(scene, cam);
    }
    loop();
  }
  startViewer().catch(() => {
    controls?.dispose();
    renderer?.dispose();
    group?.traverse(object => {
      object.geometry?.dispose();
      object.material?.dispose();
    });
    if (status) status.textContent = 'Static nominal render. Interactive 3D is unavailable in this browser; the CAD files are available below.';
  });
}
