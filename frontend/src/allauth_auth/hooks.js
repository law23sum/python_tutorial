import { useContext, useState, useEffect } from 'react'
import { AuthContext } from './AuthContext'

export function useAuth () {
  return useContext(AuthContext)?.auth
}

export function useConfig () {
  return useContext(AuthContext)?.config
}

export function useUser () {
  const auth = useContext(AuthContext)?.auth
  return authInfo(auth).user
}

export function useAuthInfo () {
  const auth = useContext(AuthContext)?.auth
  return authInfo(auth)
}

function authInfo (auth) {
  const isAuthenticated = auth.status === 200 || (auth.status === 401 && auth.meta.is_authenticated)
  const requiresReauthentication = isAuthenticated && auth.status === 401
  const pendingFlow = auth.data?.flows?.find(flow => flow.is_pending)
  return { isAuthenticated, requiresReauthentication, user: isAuthenticated ? auth.data.user : null, pendingFlow }
}

export const AuthChangeEvent = Object.freeze({
  LOGGED_OUT: 'LOGGED_OUT',
  LOGGED_IN: 'LOGGED_IN',
  REAUTHENTICATED: 'REAUTHENTICATED',
  REAUTHENTICATION_REQUIRED: 'REAUTHENTICATION_REQUIRED',
  FLOW_UPDATED: 'FLOW_UPDATED'
})

function determineAuthChangeEvent (fromAuth, toAuth) {
  let fromInfo = authInfo(fromAuth)
  const toInfo = authInfo(toAuth)
  if (toAuth.status === 410) {
    return AuthChangeEvent.LOGGED_OUT
  }
  // Corner case: user ID change. Treat as if we're transitioning from anonymous state.
  if (fromInfo.user && toInfo.user && fromInfo.user?.id !== toInfo.user?.id) {
    fromInfo = { isAuthenticated: false, requiresReauthentication: false, user: null }
  }
  if (!fromInfo.isAuthenticated && toInfo.isAuthenticated) {
    // You typically don't transition from logged out to reauthentication required.
    return AuthChangeEvent.LOGGED_IN
  } else if (fromInfo.isAuthenticated && !toInfo.isAuthenticated) {
    return AuthChangeEvent.LOGGED_OUT
  } else if (fromInfo.isAuthenticated && toInfo.isAuthenticated) {
    if (toInfo.requiresReauthentication) {
      return AuthChangeEvent.REAUTHENTICATION_REQUIRED
    } else if (fromInfo.requiresReauthentication) {
      return AuthChangeEvent.REAUTHENTICATED
    } else if (fromAuth.data.methods.length < toAuth.data.methods.length) {
      // If you do a page reload when on the reauthentication page, both fromAuth
      // and toAuth are authenticated, and it won't see the change when
      // reauthentication without this.
      return AuthChangeEvent.REAUTHENTICATED
    }
  } else if (!fromInfo.isAuthenticated && !toInfo.isAuthenticated) {
    const fromFlow = fromInfo.pendingFlow
    const toFlow = toInfo.pendingFlow
    if (toFlow?.id && fromFlow?.id !== toFlow.id) {
      return AuthChangeEvent.FLOW_UPDATED
    }
  }
  // No change.
  return null
}

export function useAuthChange () {
  const auth = useAuth()
  // Track the last auth we processed to compare against
  const [lastProcessedAuth, setLastProcessedAuth] = useState(null)
  // Track the current event separately
  const [currentEvent, setCurrentEvent] = useState(null)

  useEffect(() => {
    // First render - just store initial auth state
    if (!lastProcessedAuth) {
      setLastProcessedAuth(auth)
      return
    }

    // Compare previous and current auth states
    const event = determineAuthChangeEvent(lastProcessedAuth, auth)
    if (event) {
      setCurrentEvent(event)  // Store new event if we found one
    }

    // Update our reference point for next comparison
    setLastProcessedAuth(auth)

    // Cleanup: clear event when effect re-runs or unmounts
    return () => {
      if (event) {
        setCurrentEvent(null)
      }
    }
  }, [auth, lastProcessedAuth])

  return [auth, currentEvent]
}

export function useAuthStatus () {
  const auth = useAuth()
  return [auth, authInfo(auth)]
}
