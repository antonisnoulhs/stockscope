import { useState } from 'react'
import SearchBar from './components/SearchBar'
import MetricsGrid from './components/MetricsGrid'
import StockChart from './components/StockChart'
import CompareChart from './components/CompareChart'

const API = 'https://stockscope-backend.onrender.com'

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
}