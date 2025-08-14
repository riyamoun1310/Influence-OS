import Link from 'next/link';

export default function NavBar() {
  return (
    <nav style={{ background: 'linear-gradient(90deg, #0077b5 0%, #00c6fb 100%)', padding: '14px 0', marginBottom: 36, borderBottomLeftRadius: 18, borderBottomRightRadius: 18 }}>
      <div style={{ maxWidth: 1100, margin: '0 auto', display: 'flex', gap: 32, alignItems: 'center', justifyContent: 'space-between' }}>
  <Link href="/" style={{ color: '#fff', fontWeight: 'bold', fontSize: 24, letterSpacing: 1, textDecoration: 'none', textShadow: '0 2px 8px rgba(0,119,181,0.15)' }}>Influence-OS1</Link>
        <div style={{ display: 'flex', gap: 22 }}>
          <Link href="/dashboard" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Dashboard</Link>
          <Link href="/ask" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s', background: 'rgba(0,198,251,0.13)' }}>Ask AI</Link>
          <Link href="/article" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Article</Link>
          <Link href="/carousel" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Carousel</Link>
          <Link href="/news" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Industry News</Link>
          <Link href="/calendar" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Calendar</Link>
          <Link href="/analytics" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Analytics</Link>
          <Link href="/compliance" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>Compliance</Link>
          <Link href="/linkedin" style={{ color: '#fff', fontWeight: 500, fontSize: 16, textDecoration: 'none', padding: '6px 12px', borderRadius: 6, transition: 'background 0.2s' }}>LinkedIn Connect</Link>
        </div>
      </div>
    </nav>
  );
}
