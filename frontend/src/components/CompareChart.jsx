import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
const PERIODS = [{ label: '1M', value: '1mo' }, { label: '3M', value: '3mo' }, { label: '6M', value: '6mo' }, { label: '1Y', value: '1y' }]
const COLOR_A = '#00d4aa'; const COLOR_B = '#f97316'
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) return (
    <div style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', fontFamily: 'var(--font-data)', fontSize: 12 }}>
      <div style={{ color: 'var(--text-dim)', marginBottom: 6 }}>{label}</div>
      {payload.map(p => <div key={p.dataKey} style={{ color: p.color, marginBottom: 2 }}>{p.dataKey.toUpperCase()}: {p.value != null ? p.value.toFixed(2)+'%' : 'N/A'}</div>)}
    </div>
  )
  return null
}
function normalizeHistory(history) {
  if (!history.length) return []
  const base = history[0].close
  return history.map(d => ({ date: d.date, close: parseFloat(((d.close-base)/base*100).toFixed(2)) }))
}
function mergeHistories(dataA, tickerA, dataB, tickerB) {
  const mapB = Object.fromEntries(dataB.map(d => [d.date, d.close]))
  return dataA.map(d => ({ date: d.date, [tickerA]: d.close, [tickerB]: mapB[d.date] ?? null }))
}
const inputStyle = { background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', color: 'var(--text)', fontFamily: 'var(--font-data)', fontSize: 14, outline: 'none', width: 160, transition: 'border-color 0.2s' }
export default function CompareChart() {
  const [tickerA, setTickerA] = useState(''); const [tickerB, setTickerB] = useState('')
  const [period, setPeriod] = useState('3mo'); const [chartData, setChartData] = useState(null)
  const [loading, setLoading] = useState(false); const [error, setError] = useState(null)
  const [labels, setLabels] = useState({ a: '', b: '' })
  const handleCompare = async () => {
    const a = tickerA.trim().toUpperCase(); const b = tickerB.trim().toUpperCase()
    if (!a || !b) return setError('Enter both tickers.')
    if (a === b) return setError('Choose two different tickers.')
    setLoading(true); setError(null); setChartData(null)
    try {
      const [resA, resB] = await Promise.all([fetch(`http://localhost:8000/api/stock/${a}/history?period=${period}`), fetch(`http://localhost:8000/api/stock/${b}/history?period=${period}`)])
      const [dataA, dataB] = await Promise.all([resA.json(), resB.json()])
      if (dataA.detail) throw new Error(`${a}: ${dataA.detail}`)
      if (dataB.detail) throw new Error(`${b}: ${dataB.detail}`)
      const merged = mergeHistories(normalizeHistory(dataA), a, normalizeHistory(dataB), b)
      setChartData(merged); setLabels({ a, b })
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }
  const perfA = chartData?.[chartData.length-1]?.[labels.a]
  const perfB = chartData?.[chartData.length-1]?.[labels.b]
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, padding: '24px' }}>
      <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 20 }}>📊 Compare Two Stocks</div>
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 16 }}>
        <input value={tickerA} onChange={e => setTickerA(e.target.value.toUpperCase())} placeholder="Ticker A (e.g. AAPL)" style={inputStyle} onFocus={e => e.target.style.borderColor=COLOR_A} onBlur={e => e.target.style.borderColor='var(--border)'} />
        <span style={{ alignSelf: 'center', color: 'var(--text-dim)', fontWeight: 700 }}>vs</span>
        <input value={tickerB} onChange={e => setTickerB(e.target.value.toUpperCase())} placeholder="Ticker B (e.g. TSLA)" style={inputStyle} onFocus={e => e.target.style.borderColor=COLOR_B} onBlur={e => e.target.style.borderColor='var(--border)'} />
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          {PERIODS.map(p => <button key={p.value} onClick={() => setPeriod(p.value)} style={{ background: period===p.value ? 'var(--accent)' : 'var(--surface2)', color: period===p.value ? '#080b10' : 'var(--text-dim)', border: '1px solid var(--border)', borderRadius: 6, padding: '8px 12px', fontSize: 12, fontFamily: 'var(--font-data)', fontWeight: 600, cursor: 'pointer' }}>{p.label}</button>)}
        </div>
        <button onClick={handleCompare} disabled={loading} style={{ background: 'var(--accent)', color: '#080b10', border: 'none', borderRadius: 8, padding: '10px 20px', fontFamily: 'var(--font-ui)', fontWeight: 700, fontSize: 14, cursor: loading ? 'not-allowed' : 'pointer' }}>{loading ? 'Loading…' : 'Compare'}</button>
      </div>
      {error && <div style={{ color: 'var(--red)', fontFamily: 'var(--font-data)', fontSize: 13, marginBottom: 12 }}>⚠ {error}</div>}
      {chartData && (
        <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
          {[{ key: labels.a, color: COLOR_A, val: perfA }, { key: labels.b, color: COLOR_B, val: perfB }].map(s => (
            <div key={s.key} style={{ background: 'var(--surface2)', border: `1px solid ${s.color}33`, borderRadius: 8, padding: '8px 16px', display: 'flex', gap: 10, alignItems: 'center' }}>
              <span style={{ color: s.color, fontFamily: 'var(--font-data)', fontWeight: 700, fontSize: 14 }}>{s.key}</span>
              <span style={{ color: s.val >= 0 ? COLOR_A : 'var(--red)', fontFamily: 'var(--font-data)', fontSize: 14, fontWeight: 600 }}>{s.val >= 0 ? '+' : ''}{s.val?.toFixed(2)}%</span>
            </div>
          ))}
        </div>
      )}
      {chartData && (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#1e2d44" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{ fill: '#6b7e99', fontSize: 10, fontFamily: 'JetBrains Mono' }} tickLine={false} axisLine={false} interval="preserveStartEnd" />
            <YAxis tick={{ fill: '#6b7e99', fontSize: 10, fontFamily: 'JetBrains Mono' }} tickLine={false} axisLine={false} tickFormatter={v => `${v}%`} width={55} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontFamily: 'JetBrains Mono', fontSize: 12, paddingTop: 12 }} />
            <Line type="monotone" dataKey={labels.a} stroke={COLOR_A} strokeWidth={2} dot={false} connectNulls />
            <Line type="monotone" dataKey={labels.b} stroke={COLOR_B} strokeWidth={2} dot={false} connectNulls />
          </LineChart>
        </ResponsiveContainer>
      )}
      {!chartData && !loading && !error && (
        <div style={{ border: '1px dashed var(--border)', borderRadius: 10, padding: '40px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-data)', fontSize: 13 }}>Enter two tickers and click Compare</div>
      )}
    </div>
  )
}