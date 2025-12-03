import {
  Navigate,
  useLocation,
  useNavigate
} from 'react-router-dom'
import { useAuthChange, AuthChangeEvent, useAuthStatus } from './hooks'
import { Flows, AuthenticatorType } from '../lib/allauth'
import { useEffect, useRef } from 'react'

export const URLs = Object.freeze({
  LOGIN_URL: '/account/login',
  LOGOUT_URL: '/account/logout',
  LOGIN_REDIRECT_URL: '/',
  LOGOUT_REDIRECT_URL: '/',
})

const flow2path = {}
flow2path[Flows.LOGIN] = '/account/login'
flow2path[Flows.LOGIN_BY_CODE] = '/account/login/code/confirm'
flow2path[Flows.SIGNUP] = '/account/signup'
flow2path[Flows.VERIFY_EMAIL] = '/account/verify-email'
flow2path[Flows.PROVIDER_SIGNUP] = '/account/provider/signup'
flow2path[Flows.REAUTHENTICATE] = '/account/reauthenticate'
flow2path[`${Flows.MFA_AUTHENTICATE}:${AuthenticatorType.TOTP}`] = '/account/login/otp'
flow2path[`${Flows.MFA_AUTHENTICATE}:${AuthenticatorType.RECOVERY_CODES}`] = '/account/login/otp'
// todo: for now only support totp
// flow2path[`${Flows.MFA_AUTHENTICATE}:${AuthenticatorType.TOTP}`] = '/account/authenticate/totp'
// flow2path[`${Flows.MFA_AUTHENTICATE}:${AuthenticatorType.RECOVERY_CODES}`] = '/account/authenticate/recovery-codes'
flow2path[`${Flows.MFA_AUTHENTICATE}:${AuthenticatorType.WEBAUTHN}`] = '/account/authenticate/webauthn'
flow2path[`${Flows.MFA_REAUTHENTICATE}:${AuthenticatorType.TOTP}`] = '/account/reauthenticate/totp'
flow2path[`${Flows.MFA_REAUTHENTICATE}:${AuthenticatorType.RECOVERY_CODES}`] = '/account/reauthenticate/recovery-codes'
flow2path[`${Flows.MFA_REAUTHENTICATE}:${AuthenticatorType.WEBAUTHN}`] = '/account/reauthenticate/webauthn'
flow2path[Flows.MFA_WEBAUTHN_SIGNUP] = '/account/signup/passkey/create'

export function pathForFlow (flow, typ) {
  let key = flow.id
  if (typeof flow.types !== 'undefined') {
    typ = typ ?? flow.types[0]
    key = `${key}:${typ}`
  }
  const path = flow2path[key] ?? flow2path[flow.id]
  if (!path) {
    throw new Error(`Unknown path for flow: ${flow.id}`)
  }
  return path
}

export function pathForPendingFlow (auth) {
  const flow = auth.data.flows.find(flow => flow.is_pending)
  if (flow) {
    return pathForFlow(flow)
  }
  return null
}

function navigateToPendingFlow (auth) {
  const path = pathForPendingFlow(auth)
  if (path) {
    return <Navigate to={path} />
  }
  return null
}

export function AuthenticatedRoute ({ children }) {
  const location = useLocation()
  const [, status] = useAuthStatus()
  const next = `next=${encodeURIComponent(location.pathname + location.search)}`
  if (status.isAuthenticated) {
    return children
  } else {
    return <Navigate to={`${URLs.LOGIN_URL}?${next}`} />
  }
}

export function AnonymousRoute ({ children }) {
  /**
   * A route component that only allows unauthenticated users to access its children.
   * If a user is authenticated, they will be redirected to the login redirect URL.
   */
  const [, status] = useAuthStatus()
  if (!status.isAuthenticated) {
    return children
  } else {
    return <Navigate to={URLs.LOGIN_REDIRECT_URL} />
  }
}

export function AuthChangeRedirector ({ children }) {
  const [auth, event] = useAuthChange()
  const location = useLocation()
  const navigate = useNavigate()
  const processedEventsRef = useRef(new Set())

  useEffect(() => {
    // Only process new events
    if (event && !processedEventsRef.current.has(event)) {
      // Mark this event as handled
      processedEventsRef.current.add(event)

      switch (event) {
        case AuthChangeEvent.LOGGED_OUT:
          navigate(URLs.LOGOUT_REDIRECT_URL)
          break
        case AuthChangeEvent.LOGGED_IN:
          navigate(URLs.LOGIN_REDIRECT_URL)
          break
        case AuthChangeEvent.REAUTHENTICATED: {
          const next = new URLSearchParams(location.search).get('next') || '/'
          navigate(next)
          break
        }
        case AuthChangeEvent.REAUTHENTICATION_REQUIRED: {
          const next = `next=${encodeURIComponent(location.pathname + location.search)}`
          const path = pathForFlow(auth.data.flows[0])
          navigate(`${path}?${next}`, {
            state: { reauth: auth }
          })
          break
        }
        case AuthChangeEvent.FLOW_UPDATED: {
          const path = pathForPendingFlow(auth)
          if (!path) {
            throw new Error('No pending flow path found')
          }
          navigate(path)
          break
        }
        default:
          break
      }
    } else if (!event && !auth.meta.is_authenticated) {
      const path = pathForPendingFlow(auth);
      if (path && path !== location.pathname) {
        // Only redirect if we're not already on a more specific version of the flow path
        // This prevents e.g. /account/verify-email/<key> from redirecting to /account/verify-email/
        if (!location.pathname.startsWith(path + '/')) {
          console.log("Resuming flow", path, location.pathname);
          navigate(path);
        }
      }
    }
  }, [event, auth, location, navigate])

  return children
}

