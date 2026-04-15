import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import {
  mockPatients,
  mockDashboardStats,
  superclasseColors,
  superclasseLabels,
} from '../../services/mockData'
import styles from './DashboardPage.module.css'

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

function getCurrentDate() {
  return new Date(2026, 2, 15).toLocaleDateString('pt-BR', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

export function DashboardPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const highRiskPatients = useMemo(
    () =>
      mockPatients
        .filter(p => p.risco === 'alto')
        .sort((a, b) => (b.ultimoEcg > a.ultimoEcg ? 1 : -1))
        .slice(0, 5),
    []
  )

  const distributionData = useMemo(() => {
    const counts = {}
    mockPatients.forEach(p => {
      counts[p.superclasse] = (counts[p.superclasse] || 0) + 1
    })
    const total = mockPatients.length
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .map(([key, count]) => ({
        key,
        label: superclasseLabels[key] || key,
        count,
        pct: Math.round((count / total) * 100),
        color: superclasseColors[key],
      }))
  }, [])

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div className={styles.headerTop}>
          <h1 className={styles.title}>
            Dashboard <span className={styles.titleAccent}>Cardio-Edge-AI</span>
          </h1>
          <span className={styles.dateTag}>
            <span>&#128197;</span>
            {getCurrentDate()}
          </span>
        </div>
        <p className={styles.subtitle}>
          Bem-vindo, {user?.nome}. Aqui esta o resumo operacional do sistema CardioIA.
        </p>
      </div>

      <div className={styles.statsGrid}>
        <div className={`${styles.statCard} ${styles.navy}`}>
          <span className={styles.statIcon}>&#128101;</span>
          <span className={styles.statValue}>{mockDashboardStats.totalPacientes}</span>
          <span className={styles.statLabel}>Total de Pacientes</span>
          <span className={styles.statDesc}>Cadastrados no sistema</span>
        </div>

        <div className={`${styles.statCard} ${styles.teal}`}>
          <span className={styles.statIcon}>&#128197;</span>
          <span className={styles.statValue}>{mockDashboardStats.consultasHoje}</span>
          <span className={styles.statLabel}>Consultas Hoje</span>
          <span className={styles.statDesc}>15 de marco de 2026</span>
        </div>

        <div className={`${styles.statCard} ${styles.red}`}>
          <span className={styles.statIcon}>&#9888;</span>
          <span className={styles.statValue}>{mockDashboardStats.alertasAltoRisco}</span>
          <span className={styles.statLabel}>Alertas Alto Risco</span>
          <span className={styles.statDesc}>Requer atencao imediata</span>
        </div>

        <div className={`${styles.statCard} ${styles.purple}`}>
          <span className={styles.statIcon}>&#129302;</span>
          <span className={styles.statValue}>{mockDashboardStats.precisaoModelo}</span>
          <span className={styles.statLabel}>Precisao do Modelo</span>
          <span className={styles.statDesc}>CardioIA ECG Classifier</span>
        </div>
      </div>

      <div className={styles.grid}>
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <h2 className={styles.cardTitle}>
              <span>&#9888;</span>
              Pacientes em Alto Risco
            </h2>
            <span className={styles.cardBadge}>&#9679; Requer Atencao</span>
          </div>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Paciente</th>
                <th>Superclasse ECG</th>
                <th>Risco</th>
                <th>Ultimo ECG</th>
                <th>BPM</th>
              </tr>
            </thead>
            <tbody>
              {highRiskPatients.map(p => (
                <tr
                  key={p.id}
                  onClick={() => navigate('/pacientes')}
                  style={{ cursor: 'pointer' }}
                  title="Clique para ver todos os pacientes"
                >
                  <td>
                    <div className={styles.patientName}>{p.nome}</div>
                    <div className={styles.patientMeta}>
                      {p.idade} anos &bull; {p.sexo}
                    </div>
                  </td>
                  <td>
                    <span className={`${styles.badge} ${superclasseBadgeClass[p.superclasse]}`}>
                      {p.superclasse}
                    </span>
                  </td>
                  <td>
                    <span className={`${styles.badge} ${styles.badgeAlto}`}>
                      &#9650; Alto
                    </span>
                  </td>
                  <td>{formatDate(p.ultimoEcg)}</td>
                  <td>
                    <span className={styles.bpm}>{p.bpm}</span>
                    <span className={styles.bpmUnit}> bpm</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <h2 className={styles.cardTitle}>
              <span>&#128202;</span>
              Distribuicao por Superclasse
            </h2>
          </div>
          <div className={styles.chartArea}>
            {distributionData.map(item => (
              <div key={item.key} className={styles.chartRow}>
                <div className={styles.chartLabel}>
                  <span className={styles.chartLabelName}>
                    <span
                      className={styles.chartDot}
                      style={{ background: item.color }}
                    />
                    {item.label}
                  </span>
                  <span className={styles.chartLabelCount}>
                    {item.count} ({item.pct}%)
                  </span>
                </div>
                <div className={styles.chartTrack}>
                  <div
                    className={styles.chartFill}
                    style={{ width: `${item.pct}%`, background: item.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
