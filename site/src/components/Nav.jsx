import { useState, useEffect } from 'react';
import { motion, AnimatePresence, useScroll, useMotionValueEvent } from 'framer-motion';

export default function Nav() {
  const { scrollY } = useScroll();
  const [isVisible, setIsVisible] = useState(false);

  useMotionValueEvent(scrollY, "change", (latest) => {
    if (typeof window !== 'undefined') {
      if (latest > window.innerHeight * 0.9) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    }
  });

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.nav
          initial={{ opacity: 0, y: '-100%' }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: '-100%' }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            padding: '20px 48px',
            background: 'rgba(10, 10, 10, 0.85)',
            backdropFilter: 'blur(12px)',
            WebkitBackdropFilter: 'blur(12px)',
            borderBottom: '1px solid rgba(255, 107, 53, 0.15)',
            zIndex: 100,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <div style={{ fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '18px', color: '#fff' }}>
            PrecisionForge
          </div>
          <div style={{ display: 'flex', gap: '32px' }}>
            <a 
              href="#results" 
              style={{ color: '#888', textDecoration: 'none', transition: 'color 0.2s', fontSize: '14px' }}
              onMouseEnter={(e) => e.target.style.color = '#fff'}
              onMouseLeave={(e) => e.target.style.color = '#888'}
            >
              Results
            </a>
            <a 
              href="https://github.com/Amartya989870xxxx" 
              target="_blank" 
              rel="noopener noreferrer"
              style={{ color: '#888', textDecoration: 'none', transition: 'color 0.2s', fontSize: '14px' }}
              onMouseEnter={(e) => e.target.style.color = '#fff'}
              onMouseLeave={(e) => e.target.style.color = '#888'}
            >
              GitHub
            </a>
          </div>
        </motion.nav>
      )}
    </AnimatePresence>
  );
}
