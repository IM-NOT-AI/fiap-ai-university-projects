import { useReducer, useState } from 'react'
import { mockAppointments } from '../../services/mockData'
import { useToast } from '../../components/Toast/Toast'
import styles from './AppointmentsPage.module.css'

const TODAY = '2026-03-15'

const initialState = {
  pacienteNome: '',
  data: '',
  hora: '',
  tipo: 'Consulta',
  medico: 'Dr. Isaac Maciel',
  observacoes: '',
  errors: {},
}

function formReducer(state, action) {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        [action.field]: action.value,
        errors: { ...state.errors, [action.field]: undefined },
      }
    case 'SET_ERROR':
      return {
        ...state,
        errors: { ...state.errors, ...action.errors },
      }
    case 'RESET':
      return { ...initialState }
    default:
      return state
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const [year, month, day] = dateStr.split('-')
  return `${day}/${month}/${year}`
}

const tipoBadgeClass = {
  Consulta: styles.badgeConsulta,
  Retorno: styles.badgeRetorno,
  Urgencia: styles.badgeUrgencia,
}

const statusBadgeClass = {
  agendada: styles.badgeAgendada,
  realizada: styles.badgeRealizada,
  cancelada: styles.badgeCancelada,
}

const statusLabel = {
  agendada: '&#128197; Agendada',
  realizada: '&#10003; Realizada',
  cancelada: '&#10005; Cancelada',
}

export function AppointmentsPage() {
  const [state, dispatch] = useReducer(formReducer, initialState)
  const [appointments, setAppointments] = useState(mockAppointments)
  const [lastAdded, setLastAdded] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const { showToast, ToastContainer } = useToast()

  function validate() {
    const errors = {}
    if (!state.pacienteNome.trim()) errors.pacienteNome = 'Nome do paciente e obrigatorio.'
    if (!state.data) errors.data = 'Data e obrigatoria.'
    else if (state.data < TODAY) errors.data = 'A data nao pode estar no passado.'
    if (!state.hora) errors.hora = 'Horario e obrigatorio.'
    if (!state.tipo) errors.tipo = 'Tipo e obrigatorio.'
    if (!state.medico.trim()) errors.medico = 'Medico e obrigatorio.'
    return errors
  }

  function handleField(field) {
    return e => dispatch({ type: 'SET_FIELD', field, value: e.target.value })
  }

  function handleSubmit(e) {
    e.preventDefault()
    const errors = validate()
    if (Object.keys(errors).length > 0) {
      dispatch({ type: 'SET_ERROR', errors })
      showToast('Corrija os erros no formulario antes de continuar.', 'error')
      return
    }

    setSubmitting(true)
    setTimeout(() => {
      const newId = Date.now()
      const newAppointment = {
        id: newId,
        pacienteId: null,
        pacienteNome: state.pacienteNome.trim(),
        data: state.data,
        hora: state.hora,
        tipo: state.tipo,
        medico: state.medico.trim(),
        status: 'agendada',
        observacoes: state.observacoes.trim(),
      }

      setAppointments(prev => [newAppointment, ...prev])
      setLastAdded(newId)
      dispatch({ type: 'RESET' })
      setSubmitting(false)
      showToast(`Consulta agendada com sucesso para ${newAppointment.pacienteNome}!`, 'success')

      setTimeout(() => setLastAdded(null), 2000)
    }, 500)
  }

  function handleReset() {
    dispatch({ type: 'RESET' })
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1>Consultas</h1>
        <p>Agendamento e acompanhamento de consultas cardiologicas.</p>
      </div>

      <div className={styles.layout}>
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <h2>&#43; Agendar Nova Consulta</h2>
            <p>Preencha os dados para registrar o agendamento</p>
          </div>

          <form className={styles.form} onSubmit={handleSubmit} noValidate>
            <div className={styles.field}>
              <label className={styles.label} htmlFor="pacienteNome">
                Paciente <span className={styles.required}>*</span>
              </label>
              <input
                id="pacienteNome"
                type="text"
                className={`${styles.input} ${state.errors.pacienteNome ? styles.error : ''}`}
                value={state.pacienteNome}
                onChange={handleField('pacienteNome')}
                placeholder="Nome completo do paciente"
              />
              {state.errors.pacienteNome && (
                <span className={styles.errorText}>&#9888; {state.errors.pacienteNome}</span>
              )}
            </div>

            <div className={styles.fieldRow}>
              <div className={styles.field}>
                <label className={styles.label} htmlFor="data">
                  Data <span className={styles.required}>*</span>
                </label>
                <input
                  id="data"
                  type="date"
                  className={`${styles.input} ${state.errors.data ? styles.error : ''}`}
                  value={state.data}
                  min={TODAY}
                  onChange={handleField('data')}
                />
                {state.errors.data && (
                  <span className={styles.errorText}>&#9888; {state.errors.data}</span>
                )}
              </div>

              <div className={styles.field}>
                <label className={styles.label} htmlFor="hora">
                  Horario <span className={styles.required}>*</span>
                </label>
                <input
                  id="hora"
                  type="time"
                  className={`${styles.input} ${state.errors.hora ? styles.error : ''}`}
                  value={state.hora}
                  onChange={handleField('hora')}
                />
                {state.errors.hora && (
                  <span className={styles.errorText}>&#9888; {state.errors.hora}</span>
                )}
              </div>
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="tipo">
                Tipo <span className={styles.required}>*</span>
              </label>
              <select
                id="tipo"
                className={`${styles.select} ${state.errors.tipo ? styles.error : ''}`}
                value={state.tipo}
                onChange={handleField('tipo')}
              >
                <option value="Consulta">Consulta</option>
                <option value="Retorno">Retorno</option>
                <option value="Urgencia">Urgencia</option>
              </select>
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="medico">
                Medico Responsavel <span className={styles.required}>*</span>
              </label>
              <input
                id="medico"
                type="text"
                className={`${styles.input} ${state.errors.medico ? styles.error : ''}`}
                value={state.medico}
                onChange={handleField('medico')}
                placeholder="Nome do medico"
              />
              {state.errors.medico && (
                <span className={styles.errorText}>&#9888; {state.errors.medico}</span>
              )}
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="observacoes">
                Observacoes
              </label>
              <textarea
                id="observacoes"
                className={styles.textarea}
                value={state.observacoes}
                onChange={handleField('observacoes')}
                placeholder="Motivo da consulta, queixas, informacoes relevantes..."
              />
            </div>

            <div className={styles.btnRow}>
              <button
                type="submit"
                className={styles.submitBtn}
                disabled={submitting}
              >
                {submitting ? (
                  <span>Agendando...</span>
                ) : (
                  <>
                    <span>&#128197;</span>
                    <span>Confirmar Agendamento</span>
                  </>
                )}
              </button>
              <button
                type="button"
                className={styles.resetBtn}
                onClick={handleReset}
                title="Limpar formulario"
              >
                &#8635;
              </button>
            </div>
          </form>
        </div>

        <div className={styles.card}>
          <div className={styles.listHeader}>
            <h2>
              <span>&#128203;</span>
              Agenda de Consultas
            </h2>
            <span className={styles.countBadge}>{appointments.length}</span>
          </div>

          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Paciente</th>
                  <th>Data</th>
                  <th>Horario</th>
                  <th>Tipo</th>
                  <th>Medico</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map(a => (
                  <tr
                    key={a.id}
                    className={a.id === lastAdded ? styles.newRow : ''}
                  >
                    <td>
                      <span className={styles.patientName}>{a.pacienteNome}</span>
                    </td>
                    <td>{formatDate(a.data)}</td>
                    <td>{a.hora}</td>
                    <td>
                      <span className={`${styles.badge} ${tipoBadgeClass[a.tipo] || styles.badgeConsulta}`}>
                        {a.tipo}
                      </span>
                    </td>
                    <td>{a.medico}</td>
                    <td>
                      <span
                        className={`${styles.badge} ${statusBadgeClass[a.status] || styles.badgeAgendada}`}
                        dangerouslySetInnerHTML={{
                          __html: statusLabel[a.status] || a.status,
                        }}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <ToastContainer />
    </div>
  )
}
