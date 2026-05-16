import { motion } from 'framer-motion';
import StatCounter from './StatCounter';

export default function Results() {
  return (
    <section 
      style={{
        position: 'relative',
        minHeight: '100vh',
        backgroundColor: 'var(--bg)',
        backgroundImage: 'radial-gradient(ellipse at 80% 100%, rgba(255,107,53,0.08) 0%, transparent 60%)',
        padding: '120px 10vw',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
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
        03
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
          RESULTS
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
          Full retrieval marks. <em style={{ fontStyle: 'italic', color: 'var(--accent)' }}>First try.</em>
        </h2>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
        style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
          gap: '64px',
          marginTop: '80px',
          textAlign: 'center'
        }}
      >
        {/* Stat 1 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: 'clamp(64px, 8vw, 96px)', color: 'var(--text)', lineHeight: 1 }}>
            <StatCounter from={0} to={70} suffix="/70" duration={1500} decimals={0} />
          </div>
          <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '16px', color: 'var(--text-secondary)' }}>
            Retrieval accuracy. Full marks.
          </div>
        </div>

        {/* Stat 2 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: 'clamp(64px, 8vw, 96px)', color: 'var(--text)', lineHeight: 1 }}>
            <StatCounter from={0} to={73.05} suffix="/90" duration={1500} decimals={2} />
          </div>
          <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '16px', color: 'var(--text-secondary)' }}>
            Total automated score.
          </div>
        </div>

        {/* Stat 3 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: 'clamp(64px, 8vw, 96px)', color: 'var(--accent)', lineHeight: 1 }}>
            Δ +0.129
          </div>
          <div style={{ fontFamily: 'var(--font-body)', fontWeight: 400, fontSize: '16px', color: 'var(--text-secondary)' }}>
            Mean accuracy gain over baseline.
          </div>
        </div>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "-50px" }}
        transition={{ duration: 0.8, delay: 0.6 }}
        style={{
          fontFamily: 'var(--font-body)',
          fontWeight: 400,
          fontSize: '16px',
          color: 'var(--text-secondary)',
          textAlign: 'center',
          marginTop: '64px',
          maxWidth: '600px',
          margin: '64px auto 0'
        }}
      >
        Tested across 5 seeds with zero per-seed regressions. Consistent across arbitrary random seeds.
      </motion.p>
    </section>
  );
}
