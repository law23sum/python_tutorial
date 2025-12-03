import {FormEvent, useState} from 'react'
import FormErrors, {hasErrors} from '../components/FormErrors'
import {changePassword, requestPasswordReset} from '../lib/allauth'
import {Navigate, Link} from 'react-router-dom'
import {AllauthResponse} from "../types/allauth";
import AuthLayout from '../layouts/AuthLayout';

export default function RequestPasswordReset() {
  const [email, setEmail] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setResponse({...response, fetching: true})
    requestPasswordReset(email).then((content) => {
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
    return <Navigate to='/account/password/reset/confirm'/>
  }
  if (response.content?.status === 200) {
    return (
      <AuthLayout title="Reset Password">
        <p className={"pg-text-centered"}>Password reset sent.</p>
      </AuthLayout>
    )
  }
  return (
    <AuthLayout title="Reset Password">
      <form className="max-w-sm mx-auto" onSubmit={onSubmit}>
        <FormErrors errors={response.content?.errors} />
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
          <FormErrors param='email' errors={response.content?.errors} />
        </div>
        <div className="mt-2 flex flex-col gap-2">
          <button type="submit"
                  disabled={response.fetching}
                  className="btn btn-primary btn-block">
            Reset
          </button>
          <Link className='btn btn-block' to='/account/login'>Back to login</Link>
        </div>
      </form>
    </AuthLayout>
  )
}
