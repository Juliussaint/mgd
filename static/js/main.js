/**
 * 1. CUSTOM CURSOR LOGIC
 */
const cursorDot = document.getElementById('cursor-dot');
const cursorOutline = document.getElementById('cursor-outline');

if(cursorDot && cursorOutline) {
    window.addEventListener('mousemove', (e) => {
        const posX = e.clientX;
        const posY = e.clientY;
        cursorDot.style.left = `${posX}px`;
        cursorDot.style.top = `${posY}px`;
        cursorOutline.style.left = `${posX}px`;
        cursorOutline.style.top = `${posY}px`;
    });

    // UPDATE: Tambahkan selector baru agar cursor bereaksi di card service dan modal
    const interactiveElements = document.querySelectorAll('a, .project-card, .cta-btn, .service-card-main, .modal-content');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursorOutline.classList.add('hovered'));
        el.addEventListener('mouseleave', () => cursorOutline.classList.remove('hovered'));
    });
}

/**
 * 2. THREE.JS "DIGITAL TERRAIN" BACKGROUND
 */
const initThreeJS = () => {
    const container = document.getElementById('canvas-container');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    const geometry = new THREE.PlaneGeometry(2, 2);
    
    // MGD Brand Color Green
    const uniforms = {
        u_time: { value: 0.0 },
        u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        u_color: { value: new THREE.Color('#39FF14') } 
    };

    // Fragment Shader for Digital Grid Terrain
    const fragmentShader = `
        uniform float u_time;
        uniform vec2 u_resolution;
        uniform vec3 u_color;

        void main() {
            vec2 uv = (gl_FragCoord.xy * 2.0 - u_resolution.xy) / u_resolution.y;
            
            // Perspective warping
            vec2 p = uv;
            p.y -= 2.0; 
            p.x *= p.y * 0.5;
            
            // Moving grid lines
            float gridScale = 20.0;
            float speed = u_time * 2.0;
            
            float x = p.x * gridScale;
            float y = p.y * gridScale + speed;
            
            vec2 gv = fract(p * gridScale) - 0.5;
            
            float vx = step(0.98, abs(gv.x));
            float vy = step(0.98, abs(gv.y));
            float grid = max(vx, vy);
            
            float fade = smoothstep(0.0, 0.2, p.y) * smoothstep(4.0, 1.0, p.y);
            float fog = smoothstep(0.0, 0.5, length(uv));
            float scanline = sin(uv.y * 50.0 - u_time * 5.0) * 0.1;

            vec3 finalColor = vec3(0.0);
            finalColor += grid * u_color * fade * 0.5;
            float vignette = 1.0 - length(uv) * 0.5;
            
            gl_FragColor = vec4(finalColor * vignette + scanline * u_color * 0.2, 1.0);
        }
    `;

    const vertexShader = `
        void main() {
            gl_Position = vec4( position, 1.0 );
        }
    `;

    const material = new THREE.ShaderMaterial({
        uniforms: uniforms,
        fragmentShader: fragmentShader,
        vertexShader: vertexShader
    });

    const plane = new THREE.Mesh(geometry, material);
    scene.add(plane);

    const animate = () => {
        requestAnimationFrame(animate);
        uniforms.u_time.value += 0.005;
        renderer.render(scene, camera);
    };

    animate();

    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        uniforms.u_resolution.value.x = window.innerWidth;
        uniforms.u_resolution.value.y = window.innerHeight;
    });
};

initThreeJS();

/**
 * 3. MAGNETIC BUTTONS
 */
const magnets = document.querySelectorAll('.magnetic-area');
magnets.forEach((magnet) => {
    const content = magnet.querySelector('.magnetic-wrap');
    if(!content) return;

    magnet.addEventListener('mousemove', (e) => {
        const rect = magnet.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        content.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
    });

    magnet.addEventListener('mouseleave', () => {
        content.style.transform = 'translate(0px, 0px)';
    });
});

/**
 * 4. 3D TILT CARDS
 */
const cards = document.querySelectorAll('.tilt-card');
cards.forEach(card => {
    const glare = card.querySelector('.card-glare');
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        glare.style.opacity = '1';
        glare.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(57, 255, 20, 0.2), transparent 60%)`;
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        glare.style.opacity = '0';
    });
});

/**
 * 5. SCROLL EFFECTS
 */
const bottomBeam = document.getElementById('bottom-beam');
if(bottomBeam) {
    window.addEventListener('scroll', () => {
        const scrollTotal = document.documentElement.scrollHeight - window.innerHeight;
        const scrollCurrent = window.scrollY;
        const scrollPercentage = scrollTotal > 0 ? scrollCurrent / scrollTotal : 0;
        bottomBeam.style.opacity = 0.3 + (scrollPercentage * 0.7);
    });
}

/* --- MODAL LOGIC --- */

function openServiceModal(serviceId) {
    // 1. Ambil elemen tersembunyi
    const hiddenContentDiv = document.getElementById(`hidden-content-${serviceId}`);

    // Cek keberadaan data
    if (!hiddenContentDiv) {
        console.error("Data hidden-content ID:", serviceId, "tidak ditemukan!");
        return;
    }

    // 2. PERBAIKI KRITIS: Ambil elemen kartu yang tepat
    // Kita pakai previousElementSibling karena urutan HTML:
    // <article> (Kartu) -> lalu di bawahnya -> <div id="hidden...">
    const serviceCard = hiddenContentDiv.previousElementSibling;

    // Cek lagi jika elemen kartu tidak ketemu (misal ada komentar HTML di tengah)
    if (!serviceCard || !serviceCard.classList.contains('service-card-main')) {
        console.error("Kartu Service tidak ditemukan di sebelah hidden-content.");
        return;
    }

    // 3. Ambil elemen Modal
    const modal = document.getElementById('service-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalIcon = document.getElementById('modal-icon');
    const modalDescription = document.getElementById('modal-description');

    if (!modal) {
        console.error("Modal container tidak ditemukan di HTML.");
        return;
    }

    // 4. Ambil data dari Kartu yang DIPILIH (Bukan kartu pertama)
    const cardTitle = serviceCard.querySelector('.card-title');
    const cardIcon = serviceCard.querySelector('.service-icon-wrapper i');

    // 5. Set Data ke Modal
    if (cardTitle) modalTitle.innerText = cardTitle.innerText;
    
    // Copy class ikon
    if (cardIcon && modalIcon) {
        modalIcon.className = cardIcon.className;
    }
    
    // Masukkan HTML detail lengkap
    modalDescription.innerHTML = hiddenContentDiv.innerHTML;

    // 6. Tampilkan Modal
    modal.classList.add('active');
    
    // 7. Kunci Scroll
    document.body.style.overflow = 'hidden';
}

function closeServiceModal() {
    const modal = document.getElementById('service-modal');
    modal.classList.remove('active');
    
    // Enable scroll di body
    document.body.style.overflow = 'auto';
}

// Tutup jika klik di luar box content (di background hitam)
window.onclick = function(event) {
    const modal = document.getElementById('service-modal');
    if (event.target == modal) {
        closeServiceModal();
    }
}