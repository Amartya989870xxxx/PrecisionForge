export default function Footer() {
  return (
    <footer 
      style={{
        backgroundColor: 'var(--bg)',
        borderTop: '1px solid rgba(255, 107, 53, 0.15)',
        padding: '40px 10vw',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '24px'
      }}
    >
      <div 
        style={{ 
          fontFamily: 'var(--font-body)', 
          fontWeight: 600, 
          fontSize: '16px', 
          color: 'var(--text)' 
        }}
      >
        PrecisionForge
      </div>
      
      <div 
        style={{ 
          fontFamily: 'var(--font-body)', 
          fontWeight: 400, 
          fontSize: '14px', 
          color: 'var(--text-secondary)',
          textAlign: 'center'
        }}
      >
        Anvil P-04 · PCAM Precision Agent · 2026
      </div>
      
      <div style={{ display: 'flex', gap: '32px' }}>
        <a 
          href="https://github.com/Amartya989870xxxx" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ 
            fontFamily: 'var(--font-body)', 
            fontWeight: 400, 
            fontSize: '14px', 
            color: 'var(--text-secondary)', 
            textDecoration: 'none',
            transition: 'color 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.color = 'var(--accent)'}
          onMouseLeave={(e) => e.target.style.color = 'var(--text-secondary)'}
        >
          GitHub →
        </a>
      </div>
    </footer>
  );
}
