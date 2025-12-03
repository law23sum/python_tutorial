import {FormEvent, useState} from 'react'
import FormErrors from '../components/FormErrors'
import {getPasswordReset, resetPassword} from '../lib/allauth'
import {Navigate, Link, useLocation, useLoaderData, LoaderFunction} from 'react-router-dom'
import {AllauthResponse, FormError} from "../types/allauth";
import AuthLayout from '../layouts/AuthLayout';

export const resetPasswordByLinkLoader: LoaderFunction = async ({params}) => {
  const key = params.key
  const resp = await getPasswordReset(key)
  return {resetKey: key, resetKeyResponse: resp}
}

function ResetPassword({resetKey, resetKeyResponse}: { resetKey: string, resetKeyResponse: AllauthResponse }) {
  const [password1, setPassword1] = useState('')
  const [password2, setPassword2] = useState('')
  const [password2Errors, setPassword2Errors] = useState<FormError[]>([])

  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (password2 !== password1) {
      setPassword2Errors([{param: 'password2', message: 'Password does not match.'}])
      return
    }
    setPassword2Errors([])
    setResponse({...response, fetching: true})
    resetPassword({key: resetKey, password: password1}).then((resp) => {
      setResponse((r) => {
        return {...r, content: resp}
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

  if ([200, 401].includes(response.content?.status as number)) {
    return <Navigate to='/account/login'/>
  }
  let body
  const keyError = response.content?.errors?.filter(e => e.param === 'key')
  if (resetKeyResponse.status !== 200) {
    body = <FormErrors param='key' errors={resetKeyResponse.errors}/>
  } else if (keyError && keyError.length > 0) {
    body = <FormErrors param='key' errors={response.content?.errors}/>
  } else {
    body = (
       <form className="max-w-sm mx-auto" onSubmit={onSubmit}>
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="password">
            Password
          </label>
          <input type="password" id="password"
                 className="input input-bordered w-full"
                 autoComplete='new-password'
                 required
                 onChange={(e) => setPassword1(e.target.value)}
                 value={password1}
                 name={'password'}/>
          <FormErrors param='password' errors={response.content?.errors} />
        </div>
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="password">
            Password (again)
          </label>
          <input type="password" id="password2"
                 className="input input-bordered w-full"
                 required
                 onChange={(e) => setPassword2(e.target.value)}
                 value={password2}
                 name={'password2'}/>
          <FormErrors param='password2' errors={password2Errors} />
        </div>
        <FormErrors errors={response.content?.errors} />
        <div className="mt-2">
          <button type="submit"
                  className="btn btn-primary btn-block">
            Reset
          </button>
        </div>
      </form>
    )
  }

  return (
    <AuthLayout title="Reset Password">
      {body}
    </AuthLayout>
  )
}

export function ResetPasswordByLink() {
  const {resetKey, resetKeyResponse} = useLoaderData()
  return <ResetPassword resetKey={resetKey} resetKeyResponse={resetKeyResponse}/>
}

export function ResetPasswordByCode() {
  const {state} = useLocation()
  if (!state || !state.resetKey || !state.resetKeyResponse) {
    return <Navigate to='/account/password/reset'/>
  }
  return <ResetPassword resetKey={state.resetKey} resetKeyResponse={state.resetKeyResponse}/>
}
