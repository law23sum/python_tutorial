import {useState} from 'react'
import FormErrors from '../components/FormErrors'
import {requestLoginCode} from '../lib/allauth'
import {Navigate} from 'react-router-dom'
import {AllauthResponse} from "../types/allauth";
import AuthLayout from "../layouts/AuthLayout.tsx";

export default function RequestLoginCode() {
  const [email, setEmail] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function submit() {
    setResponse({...response, fetching: true})
    requestLoginCode(email).then((content) => {
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

  if (response.content?.status === 401) {
    return <Navigate to='/account/login/code/confirm'/>
  }
  return (
    <AuthLayout title="Mail me a sign-in code">
      <p className={"my-2"}>
        You will receive an email containing a special code for a password-free sign-in.
      </p>

      <FormErrors errors={response.content?.errors}/>
      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="email">
          Email
        </label>
        <input type="email" id="email"
               className="input input-bordered w-full"
               placeholder="name@example.com" required
               onChange={(e) => setEmail(e.target.value)}
               value={email}
               name={'email'}/>
        <FormErrors param='email' errors={response.content?.errors}/>
      </div>
      <div className="mt-2">
        <button className={"btn btn-primary btn-block"} disabled={response.fetching} onClick={() => submit()}>
          Request Code
        </button>
      </div>
    </AuthLayout>
  )
}
