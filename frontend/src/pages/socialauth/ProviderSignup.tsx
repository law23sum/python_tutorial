import {useState} from 'react'
import FormErrors, {hasErrors} from '../../components/FormErrors'
import {Link} from 'react-router-dom'
import {AllauthResponse} from "../../types/allauth";
import {providerSignup} from "../../lib/allauth";
import AuthLayout from '../../layouts/AuthLayout';

export default function ProviderSignup() {
  const [email, setEmail] = useState('')
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function submit() {
    setResponse({...response, fetching: true})
    providerSignup({email}).then((content) => {
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

  return (
    <AuthLayout title={"Sign Up"}>
      <p className={"my-2"}>
        Already have an account? <Link to='/account/login'>Login here.</Link>
      </p>

      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="email">
          Email
        </label>
        <input type="email" id="email"
               className={`input input-bordered w-full ${hasErrors({
                 errors: response.content?.errors,
                 param: 'email'
               }) ? 'input-error' : ''}`}
               placeholder="name@example.com" required
               onChange={(e) => setEmail(e.target.value)}
               value={email}
               name={'email'}/>
        <FormErrors param='email' errors={response.content?.errors}/>
      </div>
      <div className="mt-2">
        <button type="submit" disabled={response.fetching}
                onClick={() => submit()}
                className="btn btn-primary btn-block">
          Sign Up
        </button>
      </div>
    </AuthLayout>
  )
}
