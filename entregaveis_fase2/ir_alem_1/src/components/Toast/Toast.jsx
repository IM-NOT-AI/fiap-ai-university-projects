import { useState, useEffect } from 'react'
import styles from './Toast.module.css'

const ICONS = {
  success: '✓',
  error: '✕',
  info: 'ℹ',
}

export function Toast({ message, type = 'success', duration = 3000, onClose }) {
  const [hiding, setHiding] = useState(false)

  useEffect(() => {
    const hideTimer = setTimeout(() => {
      setHiding(true)
    }, duration - 300)

    const closeTimer = setTimeout(() => {
      onClose?.()
    }, duration)

    return () => {
      clearTimeout(hideTimer)
      clearTimeout(closeTimer)
    }
  }, [duration, onClose])

  function handleClose() {
    setHiding(true)
    setTimeout(() => onClose?.(), 300)
  }

  return (
    <div
      className={`${styles.toast} ${styles[type]} ${hiding ? styles.hiding : ''}`}
      role="alert"
      aria-live="polite"
    >
      <span className={styles.icon}>{ICONS[type]}</span>
      <span className={styles.message}>{message}</span>
      <button className={styles.closeBtn} onClick={handleClose} aria-label="Fechar notificacao">
        ×
      </button>
    </div>
  )
}

export function useToast() {
  const [toasts, setToasts] = useState([])

  function showToast(message, type = 'success', duration = 3000) {
    const id = Date.now() + Math.random()
    setToasts(prev => [...prev, { id, message, type, duration }])
  }

  function removeToast(id) {
    setToasts(prev => prev.filter(t => t.id !== id))
  }

  function ToastContainer() {
    return (
      <>
        {toasts.map((toast, index) => (
          <div
            key={toast.id}
            style={{ transform: `translateY(-${index * 70}px)` }}
          >
            <Toast
              message={toast.message}
              type={toast.type}
              duration={toast.duration}
              onClose={() => removeToast(toast.id)}
            />
          </div>
        ))}
      </>
    )
  }

  return { showToast, ToastContainer }
}
