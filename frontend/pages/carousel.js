import { useState } from 'react';

export default function Carousel() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [carousel, setCarousel] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateCarousel = async () => {
    setLoading(true);
    setCarousel([]);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate-carousel?email=${email}`);
    const data = await res.json();
    setCarousel(data.slides || []);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Generate LinkedIn Carousel</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} />
        <button onClick={generateCarousel} style={{ marginLeft: 8 }}>Generate Carousel</button>
      </div>
      {loading && <p>Generating carousel...</p>}
      {carousel.length > 0 && (
        <div style={{ marginTop: 24, background: '#f9f9f9', padding: 16, borderRadius: 8 }}>
          <b>Carousel Slides:</b>
          <ol>
            {carousel.map((slide, i) => (
              <li key={i}>
                <b>{slide.title}:</b> {slide.content}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}