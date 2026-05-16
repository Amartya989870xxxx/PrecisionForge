import { useEffect } from 'react';
import Lenis from '@studio-freight/lenis';
import './index.css';

import Nav from './components/Nav';
import Hero from './components/Hero';
import Problem from './components/Problem';
import HowItWorks from './components/HowItWorks';
import Results from './components/Results';
import Benchmark from './components/Benchmark';
import Footer from './components/Footer';

export default function App() {
  useEffect(() => {
    const lenis = new Lenis({ 
      duration: 1.2, 
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)) 
    });
    
    function raf(time) { 
      lenis.raf(time); 
      requestAnimationFrame(raf); 
    }
    
    requestAnimationFrame(raf);
    
    return () => lenis.destroy();
  }, []);

  return (
    <>
      <Nav />
      <Hero />
      <Problem />
      <HowItWorks />
      <Results />
      <Benchmark />
      <Footer />
    </>
  );
}
