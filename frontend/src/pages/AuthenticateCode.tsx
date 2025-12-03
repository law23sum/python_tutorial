import { useState } from 'react'
import FormErrors from '../components/FormErrors'
import * as allauth from '../lib/allauth'
import { Navigate } from 'react-router-dom'
import { useAuthInfo } from '../allauth_auth/hooks'
import AuthenticateFlow from './AuthenticateFlow'

interface AuthenticateCodeProps {
  authenticatorType: string;
  children?: React.ReactNode;
}

interface ResponseContent {
  errors?: Array<{param?: string; message: string}>;
}

export default function AuthenticateCode(props: AuthenticateCodeProps) {
  const [code, setCode] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean;
    content: ResponseContent | null;
  }>({ fetching: false, content: null })
  const authInfo = useAuthInfo()

  if (authInfo?.pendingFlow?.id !== allauth.Flows.MFA_AUTHENTICATE) {
    return <Navigate to='/' />
  }

  function submit() {
    setResponse({ ...response, fetching: true })
    allauth.mfaAuthenticate(code).then((content) => {
      setResponse((r) => { return { ...r, content } })
    }).catch((e) => {
      console.error(e)
      window.alert(e)
    }).then(() => {
      setResponse((r) => { return { ...r, fetching: false } })
    })
  }
  return (
    <AuthenticateFlow authenticatorType={props.authenticatorType}>
      {props.children}
      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="code">
          Code
        </label>
        <input type="text" id="code"
                className="input input-bordered w-full"
                placeholder="012345" required
                onChange={(e) => setCode(e.target.value)}
                value={code}
                name={'code'}/>
        <FormErrors param='code' errors={response.content?.errors} />
      </div>
      <div className="mt-2">
        <button className="btn btn-primary btn-block" onClick={() => submit()}>Sign In</button>
      </div>
    </AuthenticateFlow>
  )
}
