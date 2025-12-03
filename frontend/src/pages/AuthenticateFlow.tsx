import { Link, useNavigate } from 'react-router-dom';
import { useAuthInfo } from '../allauth_auth/hooks';
import AuthLayout from '../layouts/AuthLayout';
import { Flows } from '../lib/allauth';


interface AuthenticateFlowProps {
  authenticatorType: string;
  children?: React.ReactNode;
}

export default function AuthenticateFlow(props: AuthenticateFlowProps) {
  const authInfo = useAuthInfo()
  const navigate = useNavigate()

  if (authInfo?.pendingFlow?.id !== Flows.MFA_AUTHENTICATE) {
    navigate('/')
    return null
  }

  return (
    <AuthLayout title="Two-Factor Authentication">
      {props.children}
      {/* TODO: Add alternative options */}
      <Link className='mt-2 btn btn-block' to='/account/logout'>Cancel</Link>
    </AuthLayout>

  )
}

