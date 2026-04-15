// Servico de autenticacao para o CardioIA Portal
// Em producao chamaria o backend FastAPI em http://localhost:8000/auth/login

const MOCK_USERS = [
  {
    id: 1,
    username: 'cardiologista',
    password: 'cardio@123',
    role: 'medico',
    nome: 'Dr. Isaac Maciel',
    especialidade: 'Cardiologia Interventiva',
    crm: 'CRM-SP 98222',
  },
  {
    id: 2,
    username: 'admin',
    password: 'admin@123',
    role: 'admin',
    nome: 'Administrador do Sistema',
    especialidade: 'Gestao',
    crm: null,
  },
]

const TOKEN_KEY = 'cardioia_token'
const USER_KEY = 'cardioia_user'

function generateMockJwt(user) {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payload = btoa(
    JSON.stringify({
      sub: user.id,
      username: user.username,
      role: user.role,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + 60 * 60 * 8,
    })
  )
  const signature = btoa(`cardio-edge-ai-secret-${user.id}-${Date.now()}`)
  return `${header}.${payload}.${signature}`
}

export function loginService(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const user = MOCK_USERS.find(
        u => u.username === username && u.password === password
      )

      if (!user) {
        reject(new Error('Credenciais invalidas. Verifique usuario e senha.'))
        return
      }

      const token = generateMockJwt(user)
      const userPayload = {
        id: user.id,
        username: user.username,
        role: user.role,
        nome: user.nome,
        especialidade: user.especialidade,
        crm: user.crm,
      }

      localStorage.setItem(TOKEN_KEY, token)
      localStorage.setItem(USER_KEY, JSON.stringify(userPayload))

      resolve({ token, user: userPayload })
    }, 600)
  })
}

export function logoutService() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export function isTokenValid(token) {
  if (!token) return false
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return false
    const payload = JSON.parse(atob(parts[1]))
    return payload.exp > Math.floor(Date.now() / 1000)
  } catch {
    return false
  }
}
