import os

BASE = os.path.join(os.path.dirname(__file__), "frontend")

files = {}

files["index.html"] = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>StockScope</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>'''

files["vite.config.js"] = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({ plugins: [react()], server: { port: 5173 } })'''

files["src/main.jsx"] = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './App.css'
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode><App /></React.StrictMode>
)'''

files["src/App.css"] = ''':root {
  --bg: #080b10; --surface: #0e1420; --surface2: #141b2a;
  --border: #1e2d44; --accent: #00d4aa; --accent-dim: #00a886;
  --red: #ff4d6a; --text: #e2eaf4; --text-dim: #6b7e99;
  --font-ui: 'Syne', sans-serif; --font-data: 'JetBrains Mono', monospace;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--font-ui); min-height: 100vh; -webkit-font-smoothing: antialiased; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
.fade-in { animation: fadeIn 0.4s ease forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }'''

files["src/App.jsx"] = """import { useState } from 'react'
import SearchBar from './components/SearchBar'
import MetricsGrid from './components/MetricsGrid'
import StockChart from './components/StockChart'
import CompareChart from './components/CompareChart'

const API = 'http://localhost:8000'

export default function App() {
  const [tab, setTab] = useState('analyze')
  const [ticker, setTicker] = useState(null)
  const [stockData, setStockData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (symbol) => {
    setLoading(true); setError(null); setStockData(null); setTicker(null)
    try {
      const res = await fetch(`${API}/api/stock/${symbol}`)
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Stock not found')
      setStockData(data); setTicker(symbol)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      <header style={{ borderBottom: '1px solid var(--border)', padding: '16px 32px', display: 'flex', alignItems: 'center', gap: 16, background: 'var(--surface)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 8px var(--accent)' }} />
          <span style={{ fontFamily: 'var(--font-ui)', fontWeight: 800, fontSize: 20, letterSpacing: '-0.02em' }}>
            Stock<span style={{ color: 'var(--accent)' }}>Scope</span>
          </span>
          <span style={{ fontSize: 12, color: 'var(--text-dim)', fontFamily: 'var(--font-data)' }}>Live Market Data</span>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 4, background: 'var(--surface2)', borderRadius: 8, padding: 4 }}>
          {['analyze', 'compare'].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              background: tab === t ? 'var(--accent)' : 'transparent',
              color: tab === t ? '#080b10' : 'var(--text-dim)',
              border: 'none', borderRadius: 6, padding: '7px 18px',
              fontFamily: 'var(--font-ui)', fontWeight: 700, fontSize: 13, cursor: 'pointer'
            }}>{t === 'analyze' ? '📈 Analyze' : '⚖️ Compare'}</button>
          ))}
        </div>
      </header>

      <main style={{ maxWidth: 900, margin: '0 auto', padding: '40px 24px' }}>
        {tab === 'analyze' && (
          <>
            <div style={{ marginBottom: 40, textAlign: 'center' }}>
              <h1 style={{ fontWeight: 800, fontSize: 'clamp(26px,5vw,44px)', lineHeight: 1.1, marginBottom: 12 }}>
                Analyze any stock, <span style={{ color: 'var(--accent)' }}>instantly.</span>
              </h1>
              <p style={{ color: 'var(--text-dim)', fontSize: 16, marginBottom: 28 }}>Real-time prices, charts & key metrics from Yahoo Finance.</p>
              <div style={{ display: 'flex', justifyContent: 'center' }}>
                <SearchBar onSearch={handleSearch} loading={loading} />
              </div>
            </div>
            {error && <div style={{ background: '#1f0a10', border: '1px solid var(--red)', borderRadius: 10, padding: '14px 20px', color: 'var(--red)', fontFamily: 'var(--font-data)', fontSize: 14, marginBottom: 24 }}>⚠ {error}</div>}
            {loading && (
              <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-dim)' }}>
                <div style={{ display: 'inline-block', width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 0.7s linear infinite' }} />
                <style>{'@keyframes spin { to { transform: rotate(360deg); } }'}</style>
                <p style={{ marginTop: 16, fontFamily: 'var(--font-data)', fontSize: 14 }}>Fetching data…</p>
              </div>
            )}
            {stockData && !loading && (<><MetricsGrid data={stockData} /><StockChart ticker={ticker} /></>)}
            {!stockData && !loading && !error && (
              <div style={{ border: '1px dashed var(--border)', borderRadius: 12, padding: '60px 24px', textAlign: 'center', color: 'var(--text-dim)' }}>
                <div style={{ fontSize: 36, marginBottom: 12 }}>📈</div>
                <p style={{ fontFamily: 'var(--font-data)', fontSize: 14 }}>Search for a stock ticker to get started</p>
              </div>
            )}
          </>
        )}
        {tab === 'compare' && (
          <div className="fade-in">
            <div style={{ marginBottom: 28, textAlign: 'center' }}>
              <h1 style={{ fontWeight: 800, fontSize: 'clamp(24px,4vw,38px)', lineHeight: 1.1, marginBottom: 10 }}>
                Compare <span style={{ color: 'var(--accent)' }}>two stocks</span> side by side.
              </h1>
              <p style={{ color: 'var(--text-dim)', fontSize: 15 }}>Normalized % return — who performed better?</p>
            </div>
            <CompareChart />
          </div>
        )}
      </main>

      <footer style={{ textAlign: 'center', padding: '24px', color: 'var(--text-dim)', fontFamily: 'var(--font-data)', fontSize: 12, borderTop: '1px solid var(--border)' }}>
        StockScope · Data via Yahoo Finance · Built with FastAPI + React
      </footer>
    </div>
  )
}"""

files["src/components/SearchBar.jsx"] = """import { useState } from 'react'
const SUGGESTIONS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META']
export default function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState('')
  const handleSubmit = (e) => { e.preventDefault(); if (value.trim()) onSearch(value.trim().toUpperCase()) }
  return (
    <div style={{ width: '100%', maxWidth: 540 }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 10 }}>
        <input value={value} onChange={e => setValue(e.target.value)} placeholder="Enter ticker... (e.g. AAPL)" disabled={loading}
          style={{ flex: 1, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, padding: '12px 16px', color: 'var(--text)', fontFamily: 'var(--font-data)', fontSize: 15, outline: 'none' }}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'} onBlur={e => e.target.style.borderColor = 'var(--border)'} />
        <button type="submit" disabled={loading || !value.trim()}
          style={{ background: loading ? 'var(--accent-dim)' : 'var(--accent)', color: '#080b10', border: 'none', borderRadius: 8, padding: '12px 24px', fontFamily: 'var(--font-ui)', fontWeight: 700, fontSize: 15, cursor: loading ? 'not-allowed' : 'pointer' }}>
          {loading ? 'Loading…' : 'Search'}
        </button>
      </form>
      <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 12, color: 'var(--text-dim)', alignSelf: 'center' }}>Try:</span>
        {SUGGESTIONS.map(s => (
          <button key={s} onClick={() => { setValue(s); onSearch(s) }} disabled={loading}
            style={{ background: 'var(--surface2)', border: '1px solid var(--border)', color: 'var(--accent)', borderRadius: 6, padding: '4px 10px', fontSize: 12, fontFamily: 'var(--font-data)', cursor: 'pointer' }}>
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}"""

files["src/components/MetricsGrid.jsx"] = """const fmt = (n, type = 'number') => {
  if (n == null) return 'N/A'
  if (type === 'currency') {
    if (n >= 1e12) return `$${(n/1e12).toFixed(2)}T`
    if (n >= 1e9)  return `$${(n/1e9).toFixed(2)}B`
    if (n >= 1e6)  return `$${(n/1e6).toFixed(2)}M`
    return `$${n.toLocaleString()}`
  }
  if (type === 'percent') return `${(n*100).toFixed(2)}%`
  if (type === 'volume') {
    if (n >= 1e9) return `${(n/1e9).toFixed(1)}B`
    if (n >= 1e6) return `${(n/1e6).toFixed(1)}M`
    if (n >= 1e3) return `${(n/1e3).toFixed(1)}K`
    return n.toLocaleString()
  }
  return typeof n === 'number' ? n.toFixed(2) : n
}
function MetricCard({ label, value }) {
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '16px 20px' }}>
      <div style={{ fontSize: 11, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 6 }}>{label}</div>
      <div style={{ fontFamily: 'var(--font-data)', fontSize: 18, fontWeight: 600 }}>{value}</div>
    </div>
  )
}
export default function MetricsGrid({ data }) {
  const isPositive = data.change >= 0
  return (
    <div className="fade-in">
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, padding: '24px 28px', marginBottom: 16, display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
        <div>
          <div style={{ fontSize: 13, color: 'var(--text-dim)', marginBottom: 4 }}>{data.symbol}{data.sector ? ` · ${data.sector}` : ''}</div>
          <div style={{ fontWeight: 800, fontSize: 22 }}>{data.name}</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontFamily: 'var(--font-data)', fontWeight: 600, fontSize: 36 }}>${fmt(data.price)} <span style={{ fontSize: 14, color: 'var(--text-dim)' }}>{data.currency}</span></div>
          <div style={{ fontFamily: 'var(--font-data)', fontSize: 16, color: isPositive ? 'var(--accent)' : 'var(--red)' }}>
            {isPositive ? '▲' : '▼'} {Math.abs(data.change).toFixed(2)} ({Math.abs(data.changePercent*100).toFixed(2)}%)
          </div>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 10 }}>
        <MetricCard label="Market Cap"     value={fmt(data.marketCap, 'currency')} />
        <MetricCard label="P/E Ratio"      value={data.pe ? data.pe.toFixed(2) : 'N/A'} />
        <MetricCard label="52W High"       value={data.high52 ? `$${data.high52}` : 'N/A'} />
        <MetricCard label="52W Low"        value={data.low52  ? `$${data.low52}`  : 'N/A'} />
        <MetricCard label="Volume"         value={fmt(data.volume, 'volume')} />
        <MetricCard label="Avg Volume"     value={fmt(data.avgVolume, 'volume')} />
        <MetricCard label="Dividend Yield" value={data.dividendYield ? fmt(data.dividendYield, 'percent') : 'N/A'} />
      </div>
    </div>
  )
}"""

files["src/components/StockChart.jsx"] = """import { useState, useEffect } from 'react'
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
}"""

files["src/components/CompareChart.jsx"] = """import { useState } from 'react'
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
}"""

# Write all files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {rel_path}")

print("\n🎉 All files created! Now run: npm run dev")
