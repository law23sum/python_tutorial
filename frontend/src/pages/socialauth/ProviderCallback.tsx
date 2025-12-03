import {
  Navigate,
  useLocation,
  Link
} from 'react-router-dom'
import {URLs, pathForPendingFlow, useAuthStatus} from '../../allauth_auth'

export default function ProviderCallback() {
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const error = params.get('error')
  const [auth, status] = useAuthStatus()

  let url: string = URLs.LOGIN_URL
  if (status.isAuthenticated) {
    url = URLs.LOGIN_REDIRECT_URL
  } else {
    url = pathForPendingFlow(auth) || url
  }
  if (!error) {
    return <Navigate to={url}/>
  }
  return (
    <>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Third-Party Login Failure</h1>
      <p>Sorry, something went wrong.</p>
      <Link className="pg-link" to={url}>Back to Login</Link>
    </>
  )
}
