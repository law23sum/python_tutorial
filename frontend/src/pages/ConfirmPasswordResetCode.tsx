import {FormEvent,useState} from 'react'
import FormErrors from '../components/FormErrors'
import {getPasswordReset, Flows} from '../lib/allauth'
import {Navigate} from 'react-router-dom'
import {useAuthStatus} from '../allauth_auth'
import {AllauthResponse} from "../types/allauth";
import AuthLayout from '../layouts/AuthLayout'

export default function ConfirmPasswordResetCode() {
  const [, authInfo] = useAuthStatus()
  const [code, setCode] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function onSubmit (e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setResponse({...response, fetching: true})
    getPasswordReset(code).then((content) => {
      setResponse((r) => {
        return {...r, content}
      })
    }).catch((e) => {
      console.error(e)
      window.alert(e)
    }).then(() => {
      setResponse((r) => {
        return {...r, fetching: false}
      })
    })
  }

  if (response.content?.status === 409 || authInfo.pendingFlow?.id !== Flows.PASSWORD_RESET_BY_CODE) {
    return <Navigate to='/account/password/reset'/>
  } else if (response.content?.status === 200) {
    return <Navigate state={{resetKey: code, resetKeyResponse: response.content}}
                     to='/account/password/reset/complete'/>
  }
  return (
    <AuthLayout title="Enter Password Reset Code ">
      <p>The code expires shortly, so please enter it soon.</p>
      <form className="max-w-sm mx-auto" onSubmit={onSubmit}>
        <FormErrors errors={response.content?.errors} />
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="code">
            Code
          </label>
          <input type="code" id="code"
                 className="input input-bordered w-full"
                 required
                 onChange={(e) => setCode(e.target.value)}
                 value={code}
                 name={'code'}/>
          <FormErrors param='key' errors={response.content?.errors} />
        </div>
        <div className="mt-2">
          <button type="submit"
                  disabled={response.fetching}
                  className="btn btn-primary btn-block">
            Confirm
          </button>
        </div>
      </form>
    </AuthLayout>
  )
}
