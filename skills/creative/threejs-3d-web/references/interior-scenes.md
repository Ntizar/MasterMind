# Interiores 3D para Inmobiliaria — Patrón Completo

## Contexto
Fichas de apartamentos con interiores 3D interactivos. Datos en JSON, escena generada proceduralmente. Sin archivos GLTF externos.

## Arquitectura de la escena

```
buildInteriorScene(container, apt)
├── Scene + Camera + Renderer (1 WebGL context)
├── Lighting (ambient + directional + fill + rim)
├── Floor (wood texture procedural)
├── Per-room loop:
│   ├── Room floor (wood/tile/kitchen)
│   ├── Back wall (textured, semi-transparent)
│   ├── Left wall (first room only)
│   ├── Right wall (last room only)
│   ├── Ceiling (semi-transparent)
│   ├── Window (if not bathroom)
│   ├── Room point light
│   └── Furniture (by room type)
├── OrbitControls (damping, limits)
└── ResizeObserver
```

## Función principal

```javascript
function buildInteriorScene(container, apt) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0eeea);

    const w = container.clientWidth || 600;
    const h = container.clientHeight || 500;
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    renderer.outputEncoding = THREE.sRGBEncoding;
    container.appendChild(renderer.domElement);

    // Lighting
    scene.add(new THREE.AmbientLight(0xfff5e6, 0.6));
    const sun = new THREE.DirectionalLight(0xffeedd, 1.2);
    sun.position.set(5, 8, 3);
    sun.castShadow = true;
    sun.shadow.mapSize.set(1024, 1024);
    scene.add(sun);
    const fill = new THREE.PointLight(0xb8944d, 0.5, 20);
    fill.position.set(-3, 4, -2);
    scene.add(fill);

    const sc = 0.55; // Scale factor

    // Floor
    const floor = new THREE.Mesh(
        new THREE.PlaneGeometry(20, 20),
        new THREE.MeshStandardMaterial({ map: woodTex, roughness: 0.75, metalness: 0.05 })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Wall materials
    const wallMat = new THREE.MeshStandardMaterial({
        map: wallTex, roughness: 0.9, side: THREE.DoubleSide,
        transparent: true, opacity: 0.85
    });

    let ox = -3; // Offset X accumulator

    apt.estancias.forEach((est, idx) => {
        const rw = Math.sqrt(est.m2) * sc * 1.6;
        const rd = Math.sqrt(est.m2) * sc * 1.3;
        const rh = 2.4 * sc;
        const cx = ox + rw / 2;

        // Room floor (material varies by type)
        let rfMat;
        if (est.t === 'bath') rfMat = new THREE.MeshStandardMaterial({ map: tileTex, roughness: 0.4 });
        else if (est.t === 'kitchen') rfMat = new THREE.MeshStandardMaterial({ color: 0xd8d0c4, roughness: 0.5 });
        else rfMat = new THREE.MeshStandardMaterial({ map: woodTex, roughness: 0.75 });

        const rf = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), rfMat);
        rf.rotation.x = -Math.PI / 2;
        rf.position.set(cx, 0.01, 0);
        rf.receiveShadow = true;
        scene.add(rf);

        // Back wall
        const bw = new THREE.Mesh(new THREE.BoxGeometry(rw, rh, 0.06), wallMat);
        bw.position.set(cx, rh / 2, -rd / 2);
        bw.castShadow = true;
        scene.add(bw);

        // Side walls (cutaway: only edges)
        if (idx === 0) {
            const lw = new THREE.Mesh(new THREE.BoxGeometry(0.06, rh, rd), wallMat);
            lw.position.set(ox, rh / 2, 0);
            scene.add(lw);
        }
        if (idx === apt.estancias.length - 1) {
            const rw2 = new THREE.Mesh(new THREE.BoxGeometry(0.06, rh, rd), wallMat);
            rw2.position.set(ox + rw, rh / 2, 0);
            scene.add(rw2);
        }

        // Ceiling (semi-transparent)
        const cl = new THREE.Mesh(
            new THREE.PlaneGeometry(rw, rd),
            new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 })
        );
        cl.rotation.x = Math.PI / 2;
        cl.position.set(cx, rh, 0);
        scene.add(cl);

        // Window (not in bathrooms)
        if (est.t !== 'bath') {
            const ww = rw * 0.5, wh = rh * 0.5;
            const win = new THREE.Mesh(
                new THREE.PlaneGeometry(ww, wh),
                new THREE.MeshStandardMaterial({
                    color: 0xc8e0f0, emissive: 0xd0eaff, emissiveIntensity: 0.4,
                    transparent: true, opacity: 0.7
                })
            );
            win.position.set(cx, rh * 0.65, -rd / 2 + 0.04);
            scene.add(win);

            // Window frame
            const fM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
            // Top, bottom, left, right, center divider
            [[ww+0.08,0.03,0.04, 0, rh*0.65+wh/2],
             [ww+0.08,0.03,0.04, 0, rh*0.65-wh/2],
             [0.03,wh,0.04, -ww/2, 0],
             [0.03,wh,0.04, ww/2, 0],
             [0.03,wh,0.04, 0, 0]].forEach(([fw,fh,fd,dx,dy]) => {
                const f = new THREE.Mesh(new THREE.BoxGeometry(fw,fh,fd), fM);
                f.position.set(cx+dx, rh*0.65+dy, -rd/2+0.04);
                scene.add(f);
            });
        }

        // Room point light
        const rl = new THREE.PointLight(0xfff0dd, 0.3, rw * 2);
        rl.position.set(cx, rh - 0.1, 0);
        scene.add(rl);

        // Furniture (see below)
        buildFurniture(scene, est, cx, rw, rd, rh, apt.color);

        ox += rw + 0.15; // Gap between rooms
    });

    // Camera
    const tw = ox;
    camera.position.set(tw / 2 + 2, 4, 5);
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.target.set(tw / 2, 1.2, 0);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.minDistance = 2;
    controls.maxDistance = 12;
    controls.maxPolarAngle = Math.PI / 2.1;
    controls.update();

    // Animation
    let animId;
    function animate() {
        animId = requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    // Resize
    const ro = new ResizeObserver(() => {
        const nw = container.clientWidth, nh = container.clientHeight;
        if (nw && nh) {
            camera.aspect = nw / nh;
            camera.updateProjectionMatrix();
            renderer.setSize(nw, nh);
        }
    });
    ro.observe(container);

    return { scene, camera, renderer, controls, animId, ro };
}
```

## Muebles por tipo

### living (salón)
```javascript
// Sofá
scene.add(Object.assign(
    new THREE.Mesh(new THREE.BoxGeometry(rw*0.55, rh*0.18, rd*0.35), fabricMat),
    { position: new THREE.Vector3(cx, rh*0.18, rd*0.2), castShadow: true }
));
// Respaldos, reposabrazos, cojines...
// Mesa de centro + patas metal
// Alfombra (PlaneGeometry + material rough)
// Cuadro en pared (BoxGeometry + color accent)
```

### bed (dormitorio)
```javascript
// Frame + colchón + almohadas
// Cabecero (BoxGeometry contra pared)
// Mesitas de noche + lámparas (CylinderGeometry base + CylinderGeometry conic shade emissive)
```

### kitchen (cocina)
```javascript
// Encimera (BoxGeometry) + encimera superior
// Fregadero (BoxGeometry metal)
// Frigorífico (BoxGeometry metal, grande)
// Quemadores (CylinderGeometry flat)
```

### bath (baño)
```javascript
// Inodoro (BoxGeometry base + CylinderGeometry bowl)
// Lavabo (BoxGeometry vanity + CylinderGeometry basin)
// Espejo (PlaneGeometry metalness alto)
// Ducha (PlaneGeometry floor + PlaneGeometry glass transparent)
```

## Limpieza de escena (modal)

```javascript
function closeModal() {
    document.getElementById('modal').classList.remove('open');
    document.body.style.overflow = '';
    if (modalScene) {
        cancelAnimationFrame(modalScene.animId);   // 1. Stop animation
        modalScene.ro.disconnect();                  // 2. Disconnect observer
        // 3. Remove canvas from DOM
        if (modalScene.renderer.domElement.parentNode)
            modalScene.renderer.domElement.parentNode.removeChild(modalScene.renderer.domElement);
        modalScene.renderer.dispose();               // 4. Dispose renderer
        modalScene = null;
    }
}
```

## SVG Floor Plan Preview (alternativa a Three.js en cards)

Para listados con muchos elementos, usar SVG procedural en vez de Three.js:

```javascript
function generateFloorPlanSVG(apt, w, h) {
    const pad = 16;
    const innerW = w - pad * 2, innerH = h - pad * 2;
    const totalArea = apt.estancias.reduce((s, e) => s + e.m2, 0);
    let rects = '', labels = '';
    let x = pad;

    apt.estancias.forEach(est => {
        const ratio = est.m2 / totalArea;
        const rw = Math.max(innerW * ratio - 2, 20);
        const rh = innerH - 20;
        const color = roomColor(est.t);

        rects += `<rect x="${x}" y="${pad+10}" width="${rw}" height="${rh}"
            rx="4" fill="${color}" opacity="0.15" stroke="${color}" stroke-width="1.5"/>`;
        labels += `<text x="${x+rw/2}" y="${pad+10+rh/2-8}" text-anchor="middle"
            font-size="11" fill="${color}" font-weight="600">${est.m2} m²</text>`;
        labels += `<text x="${x+rw/2}" y="${pad+10+rh/2+8}" text-anchor="middle"
            font-size="9" fill="${color}" opacity="0.7">${roomLabel(est.t)}</text>`;

        x += rw + 4;
    });

    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">
        <rect width="${w}" height="${h}" rx="8" fill="#f8f7f5"/>
        <text x="${w/2}" y="14" text-anchor="middle" font-size="11" fill="#999">
            Apt. ${apt.n} · ${apt.m2} m²</text>
        ${rects}${labels}
    </svg>`;
}
```

## Checklist de deploy

1. [ ] Máx 2-3 contextos WebGL por página
2. [ ] SVG previews en cards, Three.js solo en hero + modal
3. [ ] Modal limpia escena al cerrar (cancelAnimationFrame + dispose + removeChild)
4. [ ] ResizeObserver en cada escena
5. [ ] Pared frontal eliminada (cutaway)
6. [ ] Techo semitransparente (opacity 0.3)
7. [ ] Iluminación: ambient cálida + directional + fill dorado + rim azul
8. [ ] Texturas procedurales (wood, tile, wall) — no dependencias externas
