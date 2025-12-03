import AuthenticateCode from './AuthenticateCode'
import { AuthenticatorType } from '../lib/allauth'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export default function AuthenticateRecoveryCodes (props: Record<string, never>) {
  return (
    <AuthenticateCode authenticatorType={AuthenticatorType.TOTP}>
      <p className="text-gray-600 my-8">
        Please enter the code from your authenticator app.
      </p>
    </AuthenticateCode>
  )
}
