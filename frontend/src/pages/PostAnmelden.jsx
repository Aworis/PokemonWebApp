import { useState, useEffect } from 'react'

export default function PostAnmelden() {
  const [abholstationen, setAbholstationen] = useState([])
  const [form, setForm] = useState({
    abholstationId: '',
    mitarbeiterName: '',
    mitarbeiterAdId: '',
    bueroNummer: '',
  })
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetch('/api/abholstationen')
      .then((r) => r.json())
      .then(setAbholstationen)
      .catch(() => {})
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setMessage(null)
    setError(null)

    try {
      const body = {
        abholstation: { id: Number(form.abholstationId) },
        mitarbeiterName: form.mitarbeiterName,
        mitarbeiterAdId: form.mitarbeiterAdId,
        bueroNummer: form.bueroNummer,
      }
      const r = await fetch('/api/auftraege', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      setMessage('Auftrag erfolgreich angemeldet!')
      setForm({ abholstationId: '', mitarbeiterName: '', mitarbeiterAdId: '', bueroNummer: '' })
    } catch (err) {
      setError('Fehler beim Anmelden: ' + err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div style={{ padding: '1.5rem', maxWidth: '480px' }}>
      <h1 style={{ fontSize: '1.5rem', color: '#21568c', marginBottom: '1rem' }}>
        📬 Post anmelden
      </h1>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
        <label style={labelStyle}>
          Abholstation
          <select
            name="abholstationId"
            value={form.abholstationId}
            onChange={handleChange}
            required
            style={inputStyle}
          >
            <option value="">– bitte wählen –</option>
            {abholstationen.map((a) => (
              <option key={a.id} value={a.id}>{a.id} – {a.name}</option>
            ))}
          </select>
        </label>

        <label style={labelStyle}>
          Mitarbeitername
          <input
            name="mitarbeiterName"
            value={form.mitarbeiterName}
            onChange={handleChange}
            required
            placeholder="Max Mustermann"
            style={inputStyle}
          />
        </label>

        <label style={labelStyle}>
          AD-ID (optional)
          <input
            name="mitarbeiterAdId"
            value={form.mitarbeiterAdId}
            onChange={handleChange}
            placeholder="mmustermann"
            style={inputStyle}
          />
        </label>

        <label style={labelStyle}>
          Büronummer
          <input
            name="bueroNummer"
            value={form.bueroNummer}
            onChange={handleChange}
            required
            placeholder="3.007"
            style={inputStyle}
          />
        </label>

        <button type="submit" disabled={submitting} style={btnStyle}>
          {submitting ? 'Wird gesendet…' : 'Auftrag anmelden'}
        </button>
      </form>

      {message && <p style={{ color: 'green', marginTop: '0.75rem' }}>{message}</p>}
      {error && <p style={{ color: 'red', marginTop: '0.75rem' }}>{error}</p>}
    </div>
  )
}

const labelStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '0.3rem',
  fontSize: '0.9rem',
  fontWeight: '500',
}

const inputStyle = {
  padding: '0.5rem',
  border: '1px solid #ccc',
  borderRadius: '4px',
  fontSize: '0.9rem',
}

const btnStyle = {
  padding: '0.65rem',
  background: '#21568c',
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '1rem',
  marginTop: '0.25rem',
}
