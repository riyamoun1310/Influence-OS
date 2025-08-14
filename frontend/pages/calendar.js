import { useState } from 'react';

export default function Calendar() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [calendar, setCalendar] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCalendar = async () => {
    setLoading(true);
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/calendar?email=${email}`);
    const data = await res.json();
    setCalendar(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Content Calendar</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} />
        <button onClick={fetchCalendar} style={{ marginLeft: 8 }}>Fetch Calendar</button>
      </div>
      {loading && <p>Loading calendar...</p>}
      {calendar.length > 0 && (
        <table style={{ width: '100%', marginTop: 24, borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>Content</th>
              <th>Scheduled Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {calendar.map((item, i) => (
              <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                <td>{item.content}</td>
                <td>{item.scheduled_time}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
