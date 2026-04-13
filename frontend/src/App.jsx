import { Routes, Route, Navigate } from 'react-router-dom'
import PostAnmelden from './pages/PostAnmelden.jsx'
import HausboteDashboard from './pages/HausboteDashboard.jsx'
import Nav from './components/Nav.jsx'

export default function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/post-anmelden" replace />} />
        <Route path="/post-anmelden" element={<PostAnmelden />} />
        <Route path="/hausbote" element={<HausboteDashboard />} />
      </Routes>
    </>
  )
}
