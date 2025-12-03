import {useState} from 'react'
import {
  useLoaderData,
  Navigate, LoaderFunction
} from 'react-router-dom'
import {getEmailVerification, verifyEmail} from '../lib/allauth'
import {AllauthResponse} from "../types/allauth";
import AuthLayout from "../layouts/AuthLayout.tsx";
import { URLs } from '../allauth_auth';

export const loader: LoaderFunction = async ({params}) => {
  const key = params.key
  const resp = await getEmailVerification(key)
  return {key, verification: resp}
}

export default function VerifyEmail() {
  const {key, verification} = useLoaderData()
  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function submit() {
    setResponse({...response, fetching: true})
    verifyEmail(key).then((content) => {
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

  if (response.content?.status && [200, 401].includes(response.content?.status)) {
    return <Navigate to={URLs.LOGIN_REDIRECT_URL}/>
  }

  let body = null
  if (verification.status === 200) {
    body = (
      <div className="space-y-6">
        <p className="text-gray-600">
          Please confirm that{' '}
          <a href={'mailto:' + verification.data.email} className="pg-link">
            {verification.data.email}
          </a>
          {' '}is an email address for user{' '}
          <span className="font-medium text-gray-900">
            {verification.data.user.display}
          </span>.
        </p>
        <button
          className="btn btn-primary btn-block"
          disabled={response.fetching}
          onClick={() => submit()}
        >
          {response.fetching ? 'Confirming...' : 'Confirm'}
        </button>
      </div>
    )
  } else if (!verification.data?.email) {
    body = <p className="text-gray-600">Invalid verification link.</p>
  } else {
    body = (
      <p className="text-gray-600">
        Unable to confirm email{' '}
        <a href={'mailto:' + verification.data.email} className="pg-link">
          {verification.data.email}
        </a>
        {' '}because it is already confirmed.
      </p>
    )
  }

  return (
    <AuthLayout title="Confirm Email Address">
      <div className="my-8">
        {body}
      </div>
    </AuthLayout>
  )
}
