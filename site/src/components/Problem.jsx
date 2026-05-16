import { motion } from 'framer-motion';

export default function Problem() {
  return (
    <motion.section 
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.7, ease: "easeOut" }}
      style={{
        position: 'relative',
        minHeight: '100vh',
        backgroundColor: 'var(--bg)',
        display: 'flex',
        alignItems: 'center',
        padding: '120px 10vw',
        overflow: 'hidden'
      }}
    >
      {/* Watermark */}
      <div 
        style={{
          position: 'absolute',
          top: '40px',
          left: '5vw',
          fontSize: '180px',
          fontFamily: 'var(--font-heading)',
          color: 'rgba(255, 255, 255, 0.03)',
          pointerEvents: 'none',
          lineHeight: 1,
          fontWeight: 700
        }}
      >
        01
      </div>

      <div style={{ display: 'flex', width: '100%', alignItems: 'center', gap: '48px', flexWrap: 'wrap' }}>
        {/* Left Column */}
        <div style={{ flex: '1 1 60%', minWidth: '320px' }}>
          <div 
            style={{ 
              fontFamily: 'var(--font-body)', 
              fontWeight: 500, 
              fontSize: '11px', 
              letterSpacing: '0.2em', 
              color: 'var(--accent)', 
              marginBottom: '24px',
              textTransform: 'uppercase'
            }}
          >
            THE PROBLEM
          </div>
          <h2 
            style={{ 
              fontFamily: 'var(--font-heading)', 
              fontWeight: 700, 
              fontSize: 'clamp(40px, 5vw, 64px)', 
              color: 'var(--text)', 
              margin: 0,
              lineHeight: 1.1,
              letterSpacing: '-0.02em'
            }}
          >
            One knob was never enough.
          </h2>
          <p 
            style={{ 
              fontFamily: 'var(--font-body)', 
              fontWeight: 400, 
              fontSize: '18px', 
              color: 'var(--text-secondary)', 
              maxWidth: '560px', 
              marginTop: '32px',
              lineHeight: 1.7
            }}
          >
            Classical Hopfield networks give you a single temperature scalar β. One number to control 64 dimensions of memory retrieval. PrecisionForge replaces it with 64 independent precision weights — one per dimension — set at inference time, without retraining.
          </p>
        </div>

        {/* Right Column */}
        <div style={{ flex: '1 1 30%', minWidth: '320px', display: 'flex', justifyContent: 'center' }}>
          <div 
            style={{ 
              position: 'relative', 
              width: '240px', 
              height: '240px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontFamily: 'var(--font-body)',
              fontWeight: 600,
              fontSize: '32px'
            }}
          >
            {/* Scalar Animation */}
            <motion.div
              animate={{ opacity: [1, 0, 0, 1] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              style={{ position: 'absolute', color: 'var(--text-secondary)' }}
            >
              β = <span style={{ color: 'var(--accent)' }}>1</span> scalar
            </motion.div>

            {/* Weights Animation */}
            <motion.div
              animate={{ opacity: [0, 1, 1, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              style={{ position: 'absolute', color: 'var(--text-secondary)' }}
            >
              Π = <span style={{ color: 'var(--accent)' }}>64</span> weights
            </motion.div>
          </div>
        </div>
      </div>
    </motion.section>
  );
}
