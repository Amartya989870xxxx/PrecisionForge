import Spline from '@splinetool/react-spline';
import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section style={{ position: 'relative', height: '100vh', width: '100%', overflow: 'hidden' }}>
      {/* Spline Background */}
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0 }}>
        <Spline scene="https://prod.spline.design/nY-Qhr7LIRp5Scfe/scene.M" />
      </div>

      {/* Dark Overlay */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0, 0, 0, 0.45)',
          zIndex: 1,
          pointerEvents: 'none'
        }}
      />

      {/* Centered Content */}
      <div
        style={{
          position: 'relative',
          zIndex: 2,
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          padding: '0 24px',
          pointerEvents: 'none'
        }}
      >
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
          style={{
            fontFamily: 'var(--font-heading)',
            fontWeight: 700,
            fontSize: 'clamp(48px, 6vw, 80px)',
            color: '#fff',
            margin: 0,
            lineHeight: 1.1,
            letterSpacing: '-0.02em'
          }}
        >
          Memory that <em style={{ fontStyle: 'italic', color: 'var(--accent)' }}>steers</em> itself.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
          style={{
            fontFamily: 'var(--font-body)',
            fontWeight: 400,
            fontSize: '20px',
            color: '#888888',
            maxWidth: '480px',
            margin: '24px auto 0',
            lineHeight: 1.6
          }}
        >
          64 precision knobs. No retraining. Inference-time control.
        </motion.p>
      </div>

      {/* Scroll Indicator */}
      <div
        style={{
          position: 'absolute',
          bottom: '40px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '12px'
        }}
      >
        <motion.div
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          style={{
            width: '2px',
            height: '48px',
            backgroundColor: 'rgba(255, 255, 255, 1)', // Opacity controlled by motion
          }}
        />
        <span
          style={{
            fontFamily: 'var(--font-body)',
            fontWeight: 400,
            fontSize: '11px',
            letterSpacing: '0.2em',
            color: '#888',
            textTransform: 'uppercase'
          }}
        >
          scroll
        </span>
      </div>
    </section>
  );
}
