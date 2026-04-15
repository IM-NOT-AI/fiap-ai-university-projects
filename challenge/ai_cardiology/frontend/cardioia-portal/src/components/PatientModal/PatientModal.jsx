import { useEffect } from 'react'
import styles from './PatientModal.module.css'
import { superclasseLabels, riskInterpretation } from '../../services/mockData'

const superclasseBadgeClass = {
  MI: styles.badgeMI,
  STTC: styles.badgeSTTC,
  CD: styles.badgeCD,
  HYP: styles.badgeHYP,
  NORM: styles.badgeNORM,
  INCONCLUSIVO: styles.badgeINCONCLUSIVO,
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const [year, month, day] = dateStr.split('-')
  return `${day}/${month}/${year}`
}

export function PatientModal({ patient, onClose }) {
  useEffect(() => {
    function handleKey(e) {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleKey)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.style.overflow = ''
    }
  }, [onClose])

  if (!patient) return null

  function handleOverlayClick(e) {
    if (e.target === e.currentTarget) onClose()
  }

  const isAlto = patient.risco === 'alto'

  return (
    <div className={styles.overlay} onClick={handleOverlayClick} role="dialog" aria-modal="true" aria-label={`Detalhes do paciente ${patient.nome}`}>
      <div className={styles.modal}>
        <div className={styles.header}>
          <div className={styles.patientInfo}>
            <h2>&#10084; {patient.nome}</h2>
            <div className={styles.patientMeta}>
              <span>{patient.idade} anos</span>
              <span>&#8226;</span>
              <span>{patient.sexo}</span>
              <span>&#8226;</span>
              <span>ID #{patient.id}</span>
            </div>
          </div>
          <button className={styles.closeBtn} onClick={onClose} aria-label="Fechar modal">
            &#215;
          </button>
        </div>

        <div className={styles.body}>
          <div className={styles.section}>
            <p className={styles.sectionTitle}>Diagnostico ECG — CardioIA</p>
            <div className={styles.badgeRow}>
              <span className={`${styles.badge} ${superclasseBadgeClass[patient.superclasse]}`}>
                {superclasseLabels[patient.superclasse] || patient.superclasse}
              </span>
              <span className={`${styles.badge} ${isAlto ? styles.badgeRiscoAlto : styles.badgeRiscoBaixo}`}>
                {isAlto ? '⚠ Alto Risco' : '✓ Baixo Risco'}
              </span>
            </div>
          </div>

          <div className={styles.section}>
            <p className={styles.sectionTitle}>Dados do Exame</p>
            <div className={styles.infoGrid}>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Ultimo ECG</span>
                <span className={styles.infoValue}>{formatDate(patient.ultimoEcg)}</span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Frequencia Cardiaca</span>
                <span className={styles.infoValue}>
                  <span className={styles.bpmValue}>{patient.bpm}</span>
                  <span className={styles.bpmUnit}> bpm</span>
                </span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>CPF</span>
                <span className={styles.infoValue}>{patient.cpf || '-'}</span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Telefone</span>
                <span className={styles.infoValue}>{patient.telefone || '-'}</span>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <p className={styles.sectionTitle}>Interpretacao IA — Cardio-Edge-AI</p>
            <div className={`${styles.iaBox} ${isAlto ? styles.alto : ''}`}>
              <p className={styles.iaText}>
                {riskInterpretation[patient.superclasse] ||
                  'Dados insuficientes para interpretacao automatica. Consultar especialista.'}
              </p>
            </div>
          </div>

          {patient.observacoes && (
            <div className={styles.section}>
              <p className={styles.sectionTitle}>Observacoes Clinicas</p>
              <div className={styles.observacoes}>{patient.observacoes}</div>
            </div>
          )}
        </div>

        <div className={styles.footer}>
          <button className={styles.btnClose} onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>
    </div>
  )
}
