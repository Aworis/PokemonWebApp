import { useState, useEffect } from 'react'

const STATUS_LABELS = {
  NEU: 'Neu',
  OFFEN: 'Offen',
  IN_BEARBEITUNG: 'In Bearbeitung',
  ABGEHOLT: 'Abgeholt',
  ERLEDIGT: 'Erledigt',
}

const STATUS_COLORS = {
  NEU: '#d4edda',
  OFFEN: '#cce5ff',
  IN_BEARBEITUNG: '#fff3cd',
  ABGEHOLT: '#e2e3e5',
  ERLEDIGT: '#e2e3e5',
}

const fmt = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('de-DE')
}

export default function HausboteDashboard() {
  const [auftraege, setAuftraege] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [exporting, setExporting] = useState(false)

  const loadAuftraege = () => {
    setLoading(true)
    setError(null)
    fetch('/api/auftraege')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((data) => {
        const sorted = [...data].sort(
          (a, b) => new Date(b.erstelltAm) - new Date(a.erstelltAm)
        )
        setAuftraege(sorted)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadAuftraege()
  }, [])

  const handleExportPdf = async () => {
    setExporting(true)
    try {
      const response = await fetch('/api/auftraege/export/pdf')
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      const disposition = response.headers.get('Content-Disposition') || ''
      const match = disposition.match(/filename="([^"]+)"/)
      a.download = match ? match[1] : 'offene-auftraege.pdf'
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      alert('PDF-Export fehlgeschlagen: ' + e.message)
    } finally {
      setExporting(false)
    }
  }

  return (
    <div style={{ padding: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h1 style={{ fontSize: '1.5rem', color: '#21568c' }}>
          📋 Hausbote – Auftragsübersicht
        </h1>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            onClick={loadAuftraege}
            style={btnStyle('#6c757d')}
            title="Aktualisieren"
          >
            🔄 Aktualisieren
          </button>
          <button
            onClick={handleExportPdf}
            disabled={exporting}
            style={btnStyle('#21568c')}
            title="Offene Aufträge als PDF exportieren"
          >
            {exporting ? 'Exportiere…' : '📄 Export PDF'}
          </button>
        </div>
      </div>

      {loading && <p>Lade Aufträge…</p>}
      {error && <p style={{ color: 'red' }}>Fehler: {error}</p>}

      {!loading && !error && (
        <>
          <p style={{ marginBottom: '0.75rem', color: '#555', fontSize: '0.9rem' }}>
            {auftraege.length} Auftrag{auftraege.length !== 1 ? 'räge' : ''} gesamt
          </p>
          <div style={{ overflowX: 'auto' }}>
            <table style={tableStyle}>
              <thead>
                <tr style={{ background: '#21568c', color: '#fff' }}>
                  <th style={th}>ID</th>
                  <th style={th}>Erstellt am</th>
                  <th style={th}>Status</th>
                  <th style={th}>Abholstation</th>
                  <th style={th}>Mitarbeiter</th>
                  <th style={th}>Büro</th>
                </tr>
              </thead>
              <tbody>
                {auftraege.map((a) => (
                  <tr key={a.id} style={{ background: STATUS_COLORS[a.status] || '#fff' }}>
                    <td style={td}>{a.id}</td>
                    <td style={td}>{fmt(a.erstelltAm)}</td>
                    <td style={td}>
                      <span style={badgeStyle(a.status)}>
                        {STATUS_LABELS[a.status] || a.status}
                      </span>
                    </td>
                    <td style={td}>
                      {a.abholstation
                        ? `${a.abholstation.id} – ${a.abholstation.name}`
                        : '–'}
                    </td>
                    <td style={td}>{a.mitarbeiterName}</td>
                    <td style={td}>{a.bueroNummer}</td>
                  </tr>
                ))}
                {auftraege.length === 0 && (
                  <tr>
                    <td colSpan={6} style={{ ...td, textAlign: 'center', color: '#888' }}>
                      Keine Aufträge vorhanden.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}

const tableStyle = {
  width: '100%',
  borderCollapse: 'collapse',
  background: '#fff',
  borderRadius: '6px',
  overflow: 'hidden',
  boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
}

const th = {
  padding: '0.7rem 1rem',
  textAlign: 'left',
  fontWeight: '600',
  fontSize: '0.9rem',
}

const td = {
  padding: '0.65rem 1rem',
  borderTop: '1px solid #dee2e6',
  fontSize: '0.9rem',
}

const badgeStyle = (status) => ({
  padding: '2px 8px',
  borderRadius: '12px',
  fontSize: '0.8rem',
  fontWeight: '600',
  background: status === 'NEU' ? '#28a745'
    : status === 'OFFEN' ? '#007bff'
    : status === 'IN_BEARBEITUNG' ? '#ffc107'
    : '#6c757d',
  color: ['NEU', 'OFFEN'].includes(status) ? '#fff' : '#333',
})

const btnStyle = (bg) => ({
  padding: '0.5rem 1rem',
  background: bg,
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '0.9rem',
})
