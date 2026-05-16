import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Benchmark() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runBenchmark = async () => {
    setLoading(true);
    setError(null);
    try {
      const API_URL = import.meta.env.VITE_API_URL || '';
      const res = await fetch(`${API_URL}/api/benchmark`);
      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRetrievalColor = (val) => {
    const num = parseFloat(val);
    if (isNaN(num)) return '#fff';
    return num >= 60 ? '#4ade80' : 'var(--accent)';
  };

  const getTotalColor = (val) => {
    const num = parseFloat(val);
    if (isNaN(num)) return '#fff';
    if (num >= 80) return '#4ade80';
    if (num >= 60) return 'var(--accent)';
    return '#ef4444';
  };

  return (
    <section 
      id="results"
      style={{
        position: 'relative',
        minHeight: '100vh',
        backgroundColor: 'var(--bg)',
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
        04
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
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
          BENCHMARK
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
          Run it yourself.
        </h2>
        <p 
          style={{ 
            fontFamily: 'var(--font-body)', 
            fontWeight: 400, 
            fontSize: '18px', 
            color: 'var(--text-secondary)', 
            maxWidth: '600px', 
            marginTop: '24px',
            lineHeight: 1.6
          }}
        >
          The full evaluation harness runs locally on your machine. Every metric below is live — not cached, not mocked.
        </p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
        style={{
          margin: '64px auto 0',
          maxWidth: '720px',
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid rgba(255,107,53,0.3)',
          borderRadius: '20px',
          padding: '56px 48px',
          boxShadow: '0 0 64px rgba(255,107,53,0.04)',
          position: 'relative'
        }}
      >
        <p style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '14px', color: '#888', fontStyle: 'italic', marginBottom: '40px', textAlign: 'center' }}>
          Warning: This benchmark simulates the environment and takes approximately 77 seconds.
        </p>

        {error && <div style={{ color: '#ef4444', textAlign: 'center', marginBottom: '24px', fontFamily: 'var(--font-body)' }}>Error: {error}</div>}

        <motion.button
          onClick={runBenchmark}
          disabled={loading}
          whileHover={!loading ? { scale: 1.01, opacity: 0.9 } : {}}
          whileTap={!loading ? { scale: 0.98 } : {}}
          animate={loading ? {
            boxShadow: ['0 0 0px rgba(255,107,53,0)', '0 0 32px rgba(255,107,53,0.6)', '0 0 0px rgba(255,107,53,0)']
          } : {}}
          transition={loading ? { duration: 2, repeat: Infinity } : { duration: 0.2 }}
          style={{
            background: 'linear-gradient(135deg, #FF6B35 0%, #CC4A1A 100%)',
            color: '#fff',
            fontFamily: 'var(--font-body)',
            fontWeight: 600,
            fontSize: '16px',
            padding: '18px 56px',
            borderRadius: '10px',
            border: 'none',
            width: '100%',
            cursor: loading ? 'wait' : 'pointer',
            opacity: loading ? 0.9 : 1,
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          {loading ? 'Running...' : 'Run Benchmark'}
        </motion.button>

        {loading && (
          <div style={{ width: '100%', height: '2px', background: 'rgba(255,255,255,0.1)', marginTop: '16px', borderRadius: '2px', overflow: 'hidden' }}>
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
              style={{ width: '30%', height: '100%', background: 'var(--accent)' }}
            />
          </div>
        )}

        <AnimatePresence>
          {metrics && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.6 }}
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                gap: '16px',
                marginTop: '40px'
              }}
            >
              {/* Mini-Card 1 */}
              <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '24px', textAlign: 'center' }}>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: '36px', color: getRetrievalColor(metrics.retrievalPts) }}>
                  {metrics.retrievalPts}
                  <span style={{ fontSize: '18px', color: '#888', fontWeight: 400 }}>/70</span>
                </div>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '13px', color: '#888', marginTop: '8px' }}>
                  Retrieval
                </div>
              </div>

              {/* Mini-Card 2 */}
              <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '24px', textAlign: 'center' }}>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: '36px', color: '#fff' }}>
                  {metrics.anisotropyPts}
                  <span style={{ fontSize: '18px', color: '#888', fontWeight: 400 }}>/20</span>
                </div>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '13px', color: '#888', marginTop: '8px' }}>
                  Anisotropy
                </div>
              </div>

              {/* Mini-Card 3 */}
              <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '24px', textAlign: 'center' }}>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: '36px', color: getTotalColor(metrics.totalAutomated) }}>
                  {metrics.totalAutomated}
                  <span style={{ fontSize: '18px', color: '#888', fontWeight: 400 }}>/90</span>
                </div>
                <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '13px', color: '#888', marginTop: '8px' }}>
                  Total
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </motion.div>
    </section>
  );
}
