import { NavLink, Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import styles from './Navbar.module.css'

function getInitials(nome) {
  if (!nome) return 'U'
  const parts = nome.replace(/^Dr[a]?\.\s*/i, '').split(' ')
  const first = parts[0]?.[0] || ''
  const last = parts[parts.length - 1]?.[0] || ''
  return (first + last).toUpperCase()
}

function getRoleLabel(role) {
  const labels = { medico: 'Medico', admin: 'Administrador' }
  return labels[role] || role
}

export function Navbar() {
  const { user, logout } = useAuth()

  return (
    <header className={styles.navbar}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          <span className={styles.logoHeart}>&#10084;</span>
          <span>
            <span className={styles.logoText}>CardioIA</span>
            <span className={styles.logoSub}>Cardio-Edge-AI</span>
          </span>
        </Link>

        <nav className={styles.nav} aria-label="Navegacao principal">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.active : ''}`
            }
          >
            <span className={styles.navIcon}>&#9732;</span>
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/pacientes"
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.active : ''}`
            }
          >
            <span className={styles.navIcon}>&#128101;</span>
            <span>Pacientes</span>
          </NavLink>

          <NavLink
            to="/consultas"
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.active : ''}`
            }
          >
            <span className={styles.navIcon}>&#128197;</span>
            <span>Consultas</span>
          </NavLink>
        </nav>

        <div className={styles.right}>
          {user && (
            <>
              <div className={styles.userInfo}>
                <span className={styles.userName}>{user.nome}</span>
                <span className={styles.userRole}>{getRoleLabel(user.role)}</span>
              </div>
              <div className={styles.avatar} title={user.nome}>
                {getInitials(user.nome)}
              </div>
              <div className={styles.divider} />
            </>
          )}
          <button className={styles.logoutBtn} onClick={logout} title="Sair do sistema">
            <span>&#8594;</span>
            <span>Sair</span>
          </button>
        </div>
      </div>
    </header>
  )
}
