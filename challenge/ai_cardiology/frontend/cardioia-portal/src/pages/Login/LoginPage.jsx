import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import styles from './LoginPage.module.css'

export function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!username.trim()) {
      setError('Informe o nome de usuario.')
      return
    }
    if (!password) {
      setError('Informe a senha.')
      return
    }

    setLoading(true)
    try {
      await login(username.trim(), password)
      navigate('/', { replace: true })
    } catch (err) {
      setError(err.message || 'Erro ao autenticar. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.logoArea}>
          <span className={styles.heart}>&#10084;</span>
          <h1 className={styles.title}>Portal CardioIA</h1>
          <p className={styles.subtitle}>Plataforma de Cardiologia Inteligente</p>
          <span className={styles.badge}>
            <span>&#9675;</span> Cardio-Edge-AI v1.0
          </span>
        </div>

        <div className={styles.divider} />

        <form className={styles.form} onSubmit={handleSubmit} noValidate>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="username">
              Usuario
            </label>
            <input
              id="username"
              type="text"
              className={`${styles.input} ${error && !username ? styles.hasError : ''}`}
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="ex: cardiologista"
              autoComplete="username"
              autoFocus
              disabled={loading}
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="password">
              Senha
            </label>
            <input
              id="password"
              type="password"
              className={`${styles.input} ${error && !password ? styles.hasError : ''}`}
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Digite sua senha"
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          {error && (
            <div className={styles.errorMsg} role="alert">
              <span>&#9888;</span>
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            className={styles.submitBtn}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className={styles.spinner} />
                <span>Autenticando...</span>
              </>
            ) : (
              <>
                <span>&#128274;</span>
                <span>Entrar no Portal</span>
              </>
            )}
          </button>
        </form>

        <div className={styles.hint}>
          <p>&#128274; Credenciais de demonstracao</p>
          <div className={styles.hintRow}>
            <span>Medico:</span>
            <span className={styles.hintKey}>cardiologista / cardio@123</span>
          </div>
          <div className={styles.hintRow}>
            <span>Admin:</span>
            <span className={styles.hintKey}>admin / admin@123</span>
          </div>
        </div>

        <div className={styles.footer}>
          FIAP — Turma 2TIAOA — RM 98222 &mdash; 2026
        </div>
      </div>
    </div>
  )
}
