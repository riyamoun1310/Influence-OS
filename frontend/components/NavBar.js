import Link from 'next/link';

export default function NavBar() {
  return (
    <nav style={{ background: '#0077b5', padding: '12px 0', marginBottom: 32 }}>
      <div style={{ maxWidth: 900, margin: '0 auto', display: 'flex', gap: 24, alignItems: 'center' }}>
        <Link href="/" style={{ color: '#fff', fontWeight: 'bold', fontSize: 20, textDecoration: 'none' }}>Influence OS</Link>
        <Link href="/dashboard" style={{ color: '#fff', textDecoration: 'none' }}>Dashboard</Link>
        <Link href="/article" style={{ color: '#fff', textDecoration: 'none' }}>Article</Link>
        <Link href="/carousel" style={{ color: '#fff', textDecoration: 'none' }}>Carousel</Link>
        <Link href="/news" style={{ color: '#fff', textDecoration: 'none' }}>Industry News</Link>
        <Link href="/calendar" style={{ color: '#fff', textDecoration: 'none' }}>Calendar</Link>
        <Link href="/analytics" style={{ color: '#fff', textDecoration: 'none' }}>Analytics</Link>
        <Link href="/compliance" style={{ color: '#fff', textDecoration: 'none' }}>Compliance</Link>
        <Link href="/linkedin" style={{ color: '#fff', textDecoration: 'none' }}>LinkedIn Connect</Link>
      </div>
    </nav>
  );
}
