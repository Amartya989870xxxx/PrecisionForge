"use client";
import { Canvas, useFrame } from "@react-three/fiber";
import { useEffect, useMemo, useRef, useState } from "react";
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
  const wrapRef = useRef<HTMLDivElement>(null);
  const [active, setActive] = useState(true);

  useEffect(() => {
    const el = wrapRef.current;
    let visible = true;
    let onScreen = true;

    const sync = () => setActive(visible && onScreen);

    const onVisibility = () => {
      visible = document.visibilityState !== "hidden";
      sync();
    };
    document.addEventListener("visibilitychange", onVisibility);

    let io: IntersectionObserver | undefined;
    if (el && typeof IntersectionObserver !== "undefined") {
      io = new IntersectionObserver(
        (entries) => {
          onScreen = entries[0]?.isIntersecting ?? true;
          sync();
        },
        { threshold: 0 },
      );
      io.observe(el);
    }

    return () => {
      document.removeEventListener("visibilitychange", onVisibility);
      io?.disconnect();
    };
  }, []);

  return (
    <div ref={wrapRef} className="h-full w-full">
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [0, 0, 10], fov: 55 }}
        frameloop={active ? "always" : "never"}
        aria-hidden
      >
        <Points />
      </Canvas>
    </div>
  );
}
