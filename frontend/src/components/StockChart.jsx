import { useState, useEffect } from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
const PERIODS = [{ label: '7D', value: '7d' }, { label: '1M', value: '1mo' }, { label: '3M', value: '3mo' }, { label: '6M', value: '6mo' }, { label: '1Y', value: '1y' }]
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) return (
    <div style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', fontFamily: 'var(--font-data)', fontSize: 13 }}>
      <div style={{ color: 'var(--text-dim)', marginBottom: 4 }}>{label}</div>
      <div style={{ color: 'var(--accent)', fontWeight: 600 }}>${payload[0].value.toFixed(2)}</div>
    </div>
  )
  return null
}
export default function StockChart({ ticker }) {
  const [period, setPeriod] = useState('1mo')
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  useEffect(() => {
    if (!ticker) return
    setLoading(true); setError(null)
    fetch(`http://localhost:8000/api/stock/${ticker}/history?period=${period}`)
      .then(r => r.json()).then(data => { if (data.detail) throw new Error(data.detail); setHistory(data) })
      .catch(e => setError(e.message)).finally(() => setLoading(false))
  }, [ticker, period])
  const isPositive = history.length > 1 ? history[history.length-1].close >= history[0].close : true
  const color = isPositive ? '#00d4aa' : '#ff4d6a'
  return (
    <div className="fade-in" style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, padding: '20px 24px', marginTop: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <div style={{ fontWeight: 700, fontSize: 16 }}>Price History</div>
        <div style={{ display: 'flex', gap: 6 }}>
          {PERIODS.map(p => (
            <button key={p.value} onClick={() => setPeriod(p.value)} style={{ background: period === p.value ? 'var(--accent)' : 'var(--surface2)', color: period === p.value ? '#080b10' : 'var(--text-dim)', border: '1px solid var(--border)', borderRadius: 6, padding: '5px 12px', fontSize: 12, fontFamily: 'var(--font-data)', fontWeight: 600, cursor: 'pointer' }}>{p.label}</button>
          ))}
        </div>
      </div>
      {loading && <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-dim)', fontFamily: 'var(--font-data)' }}>Loading chart…</div>}
      {error && <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--red)' }}>{error}</div>}
      {!loading && !error && history.length > 0 && (
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={history} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.25} />
                <stop offset="95%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#1e2d44" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{ fill: '#6b7e99', fontSize: 11, fontFamily: 'JetBrains Mono' }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
            <YAxis tick={{ fill: '#6b7e99', fontSize: 11, fontFamily: 'JetBrains Mono' }} tickLine={false} axisLine={false} tickFormatter={v => `$${v}`} domain={['auto','auto']} width={65} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="close" stroke={color} strokeWidth={2} fill="url(#colorGrad)" dot={false} activeDot={{ r: 4, fill: color }} />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}