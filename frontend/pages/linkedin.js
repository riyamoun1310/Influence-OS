export default function LinkedInAuth() {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/linkedin/login';
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Connect Your LinkedIn</h2>
      <p>To enable real profile analysis and posting, connect your LinkedIn account securely.</p>
      <button onClick={handleLogin} style={{ fontSize: 18, padding: '12px 32px', background: '#0077b5', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
        Connect with LinkedIn
      </button>
    </div>
  );
}
