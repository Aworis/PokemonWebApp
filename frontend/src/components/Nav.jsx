import { NavLink } from 'react-router-dom'

const linkStyle = ({ isActive }) => ({
  padding: '0 1rem',
  color: isActive ? '#fff' : '#cce4ff',
  fontWeight: isActive ? 'bold' : 'normal',
  textDecoration: 'none',
})

export default function Nav() {
  return (
    <nav style={{
      background: '#21568c',
      padding: '0.8rem 1.5rem',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
    }}>
      <span style={{ color: '#fff', fontWeight: 'bold', marginRight: '1rem', fontSize: '1.1rem' }}>
        📬 Hauspost
      </span>
      <NavLink to="/post-anmelden" style={linkStyle}>Post anmelden</NavLink>
      <NavLink to="/hausbote" style={linkStyle}>Hausbote Dashboard</NavLink>
    </nav>
  )
}
