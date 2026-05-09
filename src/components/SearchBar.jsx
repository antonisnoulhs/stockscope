import { useState } from 'react'

const SUGGESTIONS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META']

export default function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (value.trim()) onSearch(value.trim().toUpperCase())
  }

  return (
    <div style={{ width: '100%', maxWidth: 540 }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 10 }}>
        <input
          value={value}
          onChange={e => setValue(e.target.value)}
          placeholder="Enter ticker... (e.g. AAPL)"
          disabled={loading}
          style={{
            flex: 1,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            padding: '12px 16px',
            color: 'var(--text)',
            fontFamily: 'var(--font-data)',
            fontSize: 15,
            outline: 'none',
            transition: 'border-color 0.2s',
          }}
          onFocus={e => e.target.style.borderColor = 'var(--accent)'}
          onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
        <button
          type="submit"
          disabled={loading || !value.trim()}
          style={{
            background: loading ? 'var(--accent-dim)' : 'var(--accent)',
            color: '#080b10',
            border: 'none',
            borderRadius: 8,
            padding: '12px 24px',
            fontFamily: 'var(--font-ui)',
            fontWeight: 700,
            fontSize: 15,
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: 'background 0.2s',
            whiteSpace: 'nowrap',
          }}
        >
          {loading ? 'Loading…' : 'Search'}
        </button>
      </form>

      {/* Quick suggestions */}
      <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 12, color: 'var(--text-dim)', alignSelf: 'center' }}>Try:</span>
        {SUGGESTIONS.map(s => (
          <button
            key={s}
            onClick={() => { setValue(s); onSearch(s) }}
            disabled={loading}
            style={{
              background: 'var(--surface2)',
              border: '1px solid var(--border)',
              color: 'var(--accent)',
              borderRadius: 6,
              padding: '4px 10px',
              fontSize: 12,
              fontFamily: 'var(--font-data)',
              cursor: 'pointer',
              transition: 'border-color 0.2s',
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}