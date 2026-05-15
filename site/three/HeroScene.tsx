"use client";
import { Canvas, useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { latticePositions } from "./lattice";

function Points() {
  const ref = useRef<THREE.Points>(null);
  const positions = useMemo(() => latticePositions(2400), []);
  useFrame((s) => {
    if (!ref.current) return;
    ref.current.rotation.y = s.clock.elapsedTime * 0.05;
    ref.current.position.x = s.pointer.x * 0.6;
    ref.current.position.y = s.pointer.y * 0.4;
  });
  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial color="#f5a524" size={0.03} sizeAttenuation transparent opacity={0.85} />
    </points>
  );
}

export function HeroScene() {
  return (
    <Canvas dpr={[1, 2]} camera={{ position: [0, 0, 10], fov: 55 }} aria-hidden>
      <Points />
    </Canvas>
  );
}
