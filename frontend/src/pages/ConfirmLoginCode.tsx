import { useState } from 'react'
import FormErrors from '../components/FormErrors'
import { confirmLoginCode, Flows } from '../lib/allauth'
import { Navigate } from 'react-router-dom'
import { useAuthStatus } from '../allauth_auth'
import {AllauthResponse} from "../types/allauth";
import AuthLayout from '../layouts/AuthLayout'

export default function ConfirmLoginCode () {
  const [, authInfo] = useAuthStatus()
  const [code, setCode] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function submit () {
    setResponse({ ...response, fetching: true })
    confirmLoginCode(code).then((content) => {
      setResponse((r) => { return { ...r, content } })
    }).catch((e) => {
      console.error(e)
      window.alert(e)
    }).then(() => {
      setResponse((r) => { return { ...r, fetching: false } })
    })
  }

  if (response.content?.status === 409 || authInfo.pendingFlow?.id !== Flows.LOGIN_BY_CODE) {
    return <Navigate to='/account/login/code' />
  }
  return (
    <AuthLayout title="Enter Sign-In Code ">
      <p className={"my-2"}>
        The code expires shortly, so please enter it soon.
      </p>

      <FormErrors errors={response.content?.errors}/>
      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="code">
          Code
        </label>
        <input id="code"
               className="input input-bordered w-full"
               required
               onChange={(e) => setCode(e.target.value)}
               value={code}
               name={'code'}/>
        <FormErrors param='code' errors={response.content?.errors}/>
      </div>
      <div className="mt-2">
        <button className={"btn btn-primary btn-block"} disabled={response.fetching} onClick={() => submit()}>
          Sign In
        </button>
      </div>
    </AuthLayout>
  )
}
