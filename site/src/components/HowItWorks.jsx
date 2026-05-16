import { motion } from 'framer-motion';

const cards = [
  {
    title: "Corruption Detection",
    body: "Masked dimensions collapse toward zero. We detect them by comparing query magnitude to stored-pattern scale and amplify recovery precisely where signal is missing.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
      </svg>
    )
  },
  {
    title: "Class-Conditional Shaping",
    body: "A weighted first-pass identifies the likely attractor. Its dimension signature nudges precision without overpowering the per-query corruption map.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="22" y1="12" x2="18" y2="12" />
        <line x1="6" y1="12" x2="2" y2="12" />
        <line x1="12" y1="6" x2="12" y2="2" />
        <line x1="12" y1="22" x2="12" y2="18" />
      </svg>
    )
  },
  {
    title: "Hessian Geometry",
    body: "For near-clean probes, we solve the Theorem F3 objective: minimize κ(Π½ H Π½) via projected subgradient with four analytic warm starts.",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="3" y1="9" x2="21" y2="9" />
        <line x1="3" y1="15" x2="21" y2="15" />
        <line x1="9" y1="3" x2="9" y2="21" />
        <line x1="15" y1="3" x2="15" y2="21" />
      </svg>
    )
  }
];

export default function HowItWorks() {
  return (
    <section 
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
        02
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
          HOW IT WORKS
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
          Two regimes. <em style={{ fontStyle: 'italic', color: 'var(--accent)' }}>One</em> agent.
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
          The agent detects whether a query is corrupted or near-clean, then applies a fundamentally different precision strategy for each.
        </p>
      </motion.div>

      <div 
        style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
          gap: '24px',
          marginTop: '64px'
        }}
      >
        {cards.map((card, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-50px" }}
            transition={{ duration: 0.6, delay: idx * 0.15, ease: "easeOut" }}
            style={{
              background: 'var(--card-bg)',
              border: '1px solid var(--card-border)',
              borderRadius: '16px',
              padding: '40px 32px',
              display: 'flex',
              flexDirection: 'column',
              gap: '20px',
              transition: 'border-color 0.3s, box-shadow 0.3s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'rgba(255,107,53,0.5)';
              e.currentTarget.style.boxShadow = '0 0 32px rgba(255,107,53,0.08)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--card-border)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div>{card.icon}</div>
            <h3 
              style={{ 
                fontFamily: 'var(--font-body)', 
                fontWeight: 600, 
                fontSize: '20px', 
                color: '#fff',
                margin: 0
              }}
            >
              {card.title}
            </h3>
            <p 
              style={{ 
                fontFamily: 'var(--font-body)', 
                fontWeight: 400, 
                fontSize: '16px', 
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                margin: 0
              }}
            >
              {card.body}
            </p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
