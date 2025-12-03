import {FormEvent, useState} from "react";
import {AuthProcess, signUp} from "../lib/allauth.js";
import FormErrors, { hasErrors } from "../components/FormErrors.tsx";
import AuthLayout from "../layouts/AuthLayout.tsx";
import {AllauthResponse, Provider} from "../types/allauth";
import {useConfig} from "../allauth_auth";
import ProviderList from "./socialauth/ProviderList.tsx";


export default function SignupPage() {
  const [email, changeEmail] = useState('');
  const [password, changePassword] = useState('');
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({ fetching: false, content: null })
  const config = useConfig()
  const hasProviders = config.data.socialaccount?.providers?.filter((p: Provider) => p.client_id).length > 0


  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    signUp({ email, password: password }).then((content) => {
      setResponse((r) => { return { ...r, content } })
    }).catch((e) => {
      console.error(e)
      window.alert(e)
    }).then(() => {
      setResponse((r) => { return { ...r, fetching: false } })
    })
  }

  return (
    <AuthLayout title="Sign Up">
      <form className="max-w-sm mx-auto" onSubmit={onSubmit}>
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="email">
            Email
          </label>
          <input type="email" id="email"
                  className={`input input-bordered w-full ${hasErrors({errors: response.content?.errors, param: 'email'}) ? 'input-error' : ''}`}
                  placeholder="name@example.com" required
                  onChange={(e) => changeEmail(e.target.value)}
                  value={email}
                  name={'email'}/>
          <FormErrors param='email' errors={response.content?.errors} />
        </div>
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="password">
            Password
          </label>
          <input type="password" id="password"
                  className={`input input-bordered w-full ${hasErrors({errors: response.content?.errors, param: 'password'}) ? 'input-error' : ''}`}
                  required
                  onChange={(e) => changePassword(e.target.value)}
                  value={password}
                  name={'password'}/>
          <FormErrors param='password' errors={response.content?.errors} />
        </div>
        <FormErrors errors={response.content?.errors} />
        <div className="mt-2">
          <button type="submit"
                  className="btn btn-primary btn-block">
            Sign Up
          </button>
        </div>
      </form>
      {hasProviders
        ? <>
          <p className="text-center my-2">or</p>
          <ProviderList callbackURL='/account/provider/callback' process={AuthProcess.LOGIN} />
        </>
        : null}
    </AuthLayout>
  );
}
