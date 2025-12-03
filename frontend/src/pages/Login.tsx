import {FormEvent, useState} from "react";
import {AuthProcess, login} from "../lib/allauth";
import FormErrors from "../components/FormErrors";
import AuthLayout from "../layouts/AuthLayout";
import {AllauthResponse, Provider} from "../types/allauth";
import { useConfig } from "../allauth_auth";
import ProviderList from "./socialauth/ProviderList.tsx";
import {Link} from "react-router-dom";

export default function LoginPage() {
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
    setResponse({ fetching: true, content: null })

    login({ email, password })
      .then((content) => {
        setResponse({ fetching: false, content })
      })
      .catch((e) => {
        console.error(e)
        window.alert(e)
        setResponse({ fetching: false, content: null })
      })
  }

  return (
    <AuthLayout title="Sign In">
      <form className="max-w-sm mx-auto" onSubmit={onSubmit}>
        <FormErrors errors={response.content?.errors} />
        <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="email">
            Email
          </label>
          <input type="email" id="email"
                 className="input input-bordered w-full"
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
                 className="input input-bordered w-full"
                 required
                 onChange={(e) => changePassword(e.target.value)}
                 value={password}
                 name={'password'}/>
          <p className={"text-right pg-text-muted"}>
            <Link className='text-sm muted-link' to='/account/password/reset'>Forgot your password?</Link>
          </p>
          <FormErrors param='password' errors={response.content?.errors} />
        </div>
        <div className="mt-2">
          <button type="submit"
                  className="btn btn-primary btn-block">
            Sign In
          </button>
        </div>
      </form>
      {hasProviders
        ? <>
          <p className="text-center my-2">or</p>
          <ProviderList callbackURL='/account/provider/callback' process={AuthProcess.LOGIN} />
        </>
        : null}
      {config.data.account.login_by_code_enabled
        ? <p className={"pg-text-centered pg-text-muted"}>
          <Link className='text-sm muted-link' to='/account/login/code'>Mail me a sign-in code</Link>
        </p>
        : null}
    </AuthLayout>
  );
}
