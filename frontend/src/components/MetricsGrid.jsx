const fmt = (n, type = 'number') => {
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
}