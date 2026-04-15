import { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { mockPatients } from '../../services/mockData'
import { PatientModal } from '../../components/PatientModal/PatientModal'
import styles from './PatientsPage.module.css'

const PAGE_SIZE = 8

const superclasseBadgeClass = {
  MI: styles.badgeMI,
  STTC: styles.badgeSTTC,
  CD: styles.badgeCD,
  HYP: styles.badgeHYP,
  NORM: styles.badgeNORM,
  INCONCLUSIVO: styles.badgeINCONCLUSIVO,
}

const COLUMNS = [
  { key: 'nome', label: 'Nome' },
  { key: 'idade', label: 'Idade' },
  { key: 'sexo', label: 'Sexo' },
  { key: 'superclasse', label: 'Superclasse ECG' },
  { key: 'risco', label: 'Risco' },
  { key: 'ultimoEcg', label: 'Ultimo ECG' },
  { key: 'bpm', label: 'BPM' },
]

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const [year, month, day] = dateStr.split('-')
  return `${day}/${month}/${year}`
}

export function PatientsPage() {
  const [search, setSearch] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [sortKey, setSortKey] = useState('nome')
  const [sortDir, setSortDir] = useState('asc')
  const [selectedPatient, setSelectedPatient] = useState(null)
  const navigate = useNavigate()

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim()
    const result = q
      ? mockPatients.filter(p => p.nome.toLowerCase().includes(q))
      : [...mockPatients]

    return result.sort((a, b) => {
      const va = a[sortKey]
      const vb = b[sortKey]
      if (va === undefined) return 1
      if (vb === undefined) return -1
      const cmp = typeof va === 'number' ? va - vb : String(va).localeCompare(String(vb))
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [search, sortKey, sortDir])

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const safePage = Math.min(currentPage, totalPages)
  const paged = filtered.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE)

  function handleSearch(e) {
    setSearch(e.target.value)
    setCurrentPage(1)
  }

  function handleSort(key) {
    if (sortKey === key) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
    setCurrentPage(1)
  }

  function pageRange() {
    const pages = []
    const start = Math.max(1, safePage - 2)
    const end = Math.min(totalPages, safePage + 2)
    for (let i = start; i <= end; i++) pages.push(i)
    return pages
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div className={styles.titleArea}>
          <h1>Pacientes</h1>
          <p>Gerenciamento e monitoramento dos pacientes cadastrados no CardioIA.</p>
        </div>
        <button
          className={styles.btnNew}
          onClick={() => navigate('/consultas')}
        >
          <span>&#43;</span>
          <span>Nova Consulta</span>
        </button>
      </div>

      <div className={styles.toolbar}>
        <div className={styles.searchWrapper}>
          <span className={styles.searchIcon}>&#128269;</span>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Buscar por nome do paciente..."
            value={search}
            onChange={handleSearch}
            aria-label="Buscar paciente"
          />
        </div>
        <span className={styles.resultCount}>
          <strong>{filtered.length}</strong> paciente{filtered.length !== 1 ? 's' : ''} encontrado{filtered.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className={styles.card}>
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                {COLUMNS.map(col => (
                  <th key={col.key} onClick={() => handleSort(col.key)}>
                    {col.label}
                    <span className={`${styles.sortIcon} ${sortKey === col.key ? styles.active : ''}`}>
                      {sortKey === col.key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ' ↕'}
                    </span>
                  </th>
                ))}
                <th>Acoes</th>
              </tr>
            </thead>
            <tbody>
              {paged.length === 0 ? (
                <tr>
                  <td colSpan={8}>
                    <div className={styles.emptyState}>
                      <span className={styles.emptyIcon}>&#128269;</span>
                      <p className={styles.emptyText}>Nenhum paciente encontrado</p>
                      <p className={styles.emptySub}>Tente um termo de busca diferente.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                paged.map(p => (
                  <tr key={p.id}>
                    <td>
                      <span className={styles.patientName}>{p.nome}</span>
                    </td>
                    <td>{p.idade} anos</td>
                    <td>{p.sexo}</td>
                    <td>
                      <span className={`${styles.badge} ${superclasseBadgeClass[p.superclasse]}`}>
                        {p.superclasse}
                      </span>
                    </td>
                    <td>
                      <span className={`${styles.badge} ${p.risco === 'alto' ? styles.badgeAlto : styles.badgeBaixo}`}>
                        {p.risco === 'alto' ? '⚠ Alto' : '✓ Baixo'}
                      </span>
                    </td>
                    <td>{formatDate(p.ultimoEcg)}</td>
                    <td>
                      <span className={styles.bpm}>{p.bpm}</span>
                      <span className={styles.bpmUnit}> bpm</span>
                    </td>
                    <td>
                      <button
                        className={styles.btnDetail}
                        onClick={() => setSelectedPatient(p)}
                      >
                        Ver detalhes
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {filtered.length > PAGE_SIZE && (
          <div className={styles.pagination}>
            <span className={styles.pageInfo}>
              Mostrando{' '}
              <strong>
                {(safePage - 1) * PAGE_SIZE + 1}
                {' - '}
                {Math.min(safePage * PAGE_SIZE, filtered.length)}
              </strong>{' '}
              de <strong>{filtered.length}</strong>
            </span>
            <div className={styles.pageButtons}>
              <button
                className={styles.pageBtn}
                onClick={() => setCurrentPage(1)}
                disabled={safePage === 1}
                aria-label="Primeira pagina"
              >
                &#171;
              </button>
              <button
                className={styles.pageBtn}
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={safePage === 1}
                aria-label="Pagina anterior"
              >
                &#8249;
              </button>
              {pageRange().map(n => (
                <button
                  key={n}
                  className={`${styles.pageBtn} ${n === safePage ? styles.activePage : ''}`}
                  onClick={() => setCurrentPage(n)}
                >
                  {n}
                </button>
              ))}
              <button
                className={styles.pageBtn}
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={safePage === totalPages}
                aria-label="Proxima pagina"
              >
                &#8250;
              </button>
              <button
                className={styles.pageBtn}
                onClick={() => setCurrentPage(totalPages)}
                disabled={safePage === totalPages}
                aria-label="Ultima pagina"
              >
                &#187;
              </button>
            </div>
          </div>
        )}
      </div>

      {selectedPatient && (
        <PatientModal
          patient={selectedPatient}
          onClose={() => setSelectedPatient(null)}
        />
      )}
    </div>
  )
}
