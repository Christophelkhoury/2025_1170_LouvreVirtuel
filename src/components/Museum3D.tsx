import React, { useRef, useState, useCallback, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, useTexture, Environment, SpotLight } from '@react-three/drei';
import * as THREE from 'three';
import { Painting, GeneratedPainting } from '../types';
import { Maximize2, Minimize2 } from 'lucide-react';

interface FrameProps {
  size: [number, number];
  position: [number, number, number];
}

function Frame({ size, position }: FrameProps) {
  const [width, height] = size;
  const frameWidth = 0.1;

  return (
    <group position={position}>
      <mesh position={[0, height/2 + frameWidth/2, 0]}>
        <boxGeometry args={[width + frameWidth*2, frameWidth, frameWidth]} />
        <meshStandardMaterial color="#8b4513" />
      </mesh>
      <mesh position={[0, -height/2 - frameWidth/2, 0]}>
        <boxGeometry args={[width + frameWidth*2, frameWidth, frameWidth]} />
        <meshStandardMaterial color="#8b4513" />
      </mesh>
      <mesh position={[-width/2 - frameWidth/2, 0, 0]}>
        <boxGeometry args={[frameWidth, height + frameWidth*2, frameWidth]} />
        <meshStandardMaterial color="#8b4513" />
      </mesh>
      <mesh position={[width/2 + frameWidth/2, 0, 0]}>
        <boxGeometry args={[frameWidth, height + frameWidth*2, frameWidth]} />
        <meshStandardMaterial color="#8b4513" />
      </mesh>
    </group>
  );
}

interface PaintingMeshProps {
  painting: Painting | GeneratedPainting;
  position: [number, number, number];
}

function PaintingMesh({ painting, position }: PaintingMeshProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const materialRef = useRef<THREE.MeshStandardMaterial>(null);
  const { gl } = useThree();

  React.useEffect(() => {
    // Create a new texture loader
    const loader = new THREE.TextureLoader();
    
    // Configure the loader
    loader.setCrossOrigin('anonymous');
    
    // Load the texture
    loader.load(
      painting.imageUrl,
      (texture) => {
        // Configure texture
        texture.encoding = THREE.sRGBEncoding;
        texture.flipY = true; // Changed from false to true
        texture.needsUpdate = true;

        // Update material with loaded texture
        if (materialRef.current) {
          materialRef.current.map = texture;
          materialRef.current.needsUpdate = true;
        }
        
        setIsLoaded(true);
        setHasError(false);
      },
      undefined,
      (error) => {
        console.error('Error loading texture:', error);
        setHasError(true);
        setIsLoaded(false);
      }
    );

    // Cleanup
    return () => {
      if (materialRef.current?.map) {
        materialRef.current.map.dispose();
      }
    };
  }, [painting.imageUrl, gl]);

  return (
    <group position={position}>
      {/* Painting mesh */}
      <mesh>
        <planeGeometry args={[4, 3]} />
        <meshStandardMaterial 
          ref={materialRef}
          color={hasError ? "#ff6b6b" : "#cccccc"}
          transparent
          opacity={isLoaded ? 1 : 0.5}
        />
      </mesh>

      {/* Frame */}
      <Frame size={[4, 3]} position={[0, 0, 0.05]} />

      {/* Lighting */}
      <SpotLight
        position={[0, 2, 2]}
        angle={0.5}
        penumbra={0.5}
        intensity={1}
        distance={10}
        castShadow
      />

      {/* Loading indicator or error message */}
      {(!isLoaded || hasError) && (
        <mesh position={[0, 0, 0.1]}>
          <planeGeometry args={[4, 3]} />
          <meshBasicMaterial color={hasError ? "#ff6b6b" : "#cccccc"} transparent opacity={0.3} />
        </mesh>
      )}
    </group>
  );
}

interface MuseumWallProps {
  position: [number, number, number];
  rotation: [number, number, number];
  painting?: Painting | GeneratedPainting;
}

function MuseumWall({ position, rotation, painting }: MuseumWallProps) {
  return (
    <group position={position} rotation={rotation}>
      {/* Wall */}
      <mesh position={[0, 0, 0]}>
        <planeGeometry args={[10, 6]} />
        <meshStandardMaterial color="#e0e0e0" />
      </mesh>
      
      {/* Baseboard */}
      <mesh position={[0, -2.5, 0.01]}>
        <planeGeometry args={[10, 1]} />
        <meshStandardMaterial color="#f5f5f5" />
      </mesh>
      
      {/* Painting */}
      {painting && (
        <group position={[0, 0, 0.1]}>
          <PaintingMesh painting={painting} position={[0, 0, 0]} />
        </group>
      )}
    </group>
  );
}

interface Museum3DProps {
  paintings: (Painting | GeneratedPainting)[];
}

export function Museum3D({ paintings }: Museum3DProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const toggleFullscreen = useCallback(() => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  }, []);

  // Ensure we have enough paintings for all walls
  const displayPaintings = [...paintings];
  while (displayPaintings.length < 4) {
    displayPaintings.push(paintings[displayPaintings.length % paintings.length]);
  }

  return (
    <div ref={containerRef} className="relative w-full h-screen">
      <button
        onClick={toggleFullscreen}
        className="absolute top-4 right-4 z-10 bg-white/80 backdrop-blur-sm p-2 rounded-lg shadow-lg hover:bg-white transition-colors"
      >
        {isFullscreen ? (
          <Minimize2 className="w-6 h-6 text-gray-800" />
        ) : (
          <Maximize2 className="w-6 h-6 text-gray-800" />
        )}
      </button>

      <Canvas
        camera={{ position: [0, 0, 5], fov: 75 }}
        shadows
        gl={{ 
          preserveDrawingBuffer: true,
          antialias: true,
          alpha: false
        }}
      >
        <Suspense fallback={null}>
          <fog attach="fog" args={['#000', 1, 25]} />
          <ambientLight intensity={0.8} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          
          {/* Front Wall */}
          <MuseumWall
            position={[0, 0, -5]}
            rotation={[0, 0, 0]}
            painting={displayPaintings[0]}
          />
          
          {/* Right Wall */}
          <MuseumWall
            position={[5, 0, 0]}
            rotation={[0, -Math.PI / 2, 0]}
            painting={displayPaintings[1]}
          />
          
          {/* Back Wall */}
          <MuseumWall
            position={[0, 0, 5]}
            rotation={[0, Math.PI, 0]}
            painting={displayPaintings[2]}
          />
          
          {/* Left Wall */}
          <MuseumWall
            position={[-5, 0, 0]}
            rotation={[0, Math.PI / 2, 0]}
            painting={displayPaintings[3]}
          />
          
          {/* Floor */}
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -3, 0]} receiveShadow>
            <planeGeometry args={[10, 10]} />
            <meshStandardMaterial color="#1a1a1a" />
          </mesh>
          
          {/* Ceiling */}
          <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 3, 0]}>
            <planeGeometry args={[10, 10]} />
            <meshStandardMaterial color="#2a2a2a" />
          </mesh>

          <Environment preset="apartment" />
          
          <OrbitControls
            enableZoom={false}
            enablePan={false}
            minPolarAngle={Math.PI / 2}
            maxPolarAngle={Math.PI / 2}
            rotateSpeed={0.5}
          />
        </Suspense>
      </Canvas>
    </div>
  );
}
