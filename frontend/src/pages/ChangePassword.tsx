import {useState} from 'react'
import FormErrors from '../components/FormErrors'
import {changePassword} from '../lib/allauth'
import {Navigate, useNavigate} from 'react-router-dom'
import {useUser} from "../allauth_auth";
import {AllauthResponse, FormError} from "../types/allauth";
import AuthLayout from "../layouts/AuthLayout.tsx";

export default function ChangePassword() {
  const navigate = useNavigate()
  const hasCurrentPassword = useUser().has_usable_password
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [newPassword2, setNewPassword2] = useState('')
  const [newPassword2Errors, setNewPassword2Errors] = useState<FormError[]>([])

  const [response, setResponse] = useState<{
    fetching: boolean,
    content: AllauthResponse | null
  }>({fetching: false, content: null})

  function submit() {
    if (newPassword !== newPassword2) {
      setNewPassword2Errors([{param: 'new_password2', message: 'Password does not match.'}])
      return
    }
    setNewPassword2Errors([])
    setResponse({...response, fetching: true})
    changePassword({current_password: currentPassword, new_password: newPassword}).then((resp) => {
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

  function cancel() {
    navigate('/dashboard/profile')
  }

  if (response.content?.status === 200) {
    return <Navigate to='/dashboard/profile'/>
  }
  return (
    <AuthLayout title={hasCurrentPassword ? 'Change Password' : 'Set Password'}>
      <p className="text-gray-600 my-8">{hasCurrentPassword ? 'Enter your current password, followed by your new password.' : 'You currently have no password set. Enter your (new) password.'}</p>
      <FormErrors errors={response.content?.errors}/>
      {hasCurrentPassword
        ? <div className="mt-2 w-full">
          <label className="label font-bold" htmlFor="current_password">
            Current password
          </label>
          <input type="password" id="current_password"
                 className="input input-bordered w-full"
                 required
                 onChange={(e) => setCurrentPassword(e.target.value)}
                 value={currentPassword}
                 autoComplete='password'
                 name={'current_password'}/>
          <FormErrors param='current_password' errors={response.content?.errors}/>
        </div>
        : null}
      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="new_password">
          Password
        </label>
        <input type="password" id="new_password"
               className="input input-bordered w-full"
               required
               onChange={(e) => setNewPassword(e.target.value)}
               value={newPassword}
               autoComplete='new-password'
               name={'new_password'}/>
        <FormErrors param='new_password' errors={response.content?.errors}/>
      </div>
      <div className="mt-2 w-full">
        <label className="label font-bold" htmlFor="new_password2">
          Password (again)
        </label>
        <input type="password" id="new_password2"
               className="input input-bordered w-full"
               required
               onChange={(e) => setNewPassword2(e.target.value)}
               value={newPassword2}
               name={'new_password2'}/>
        <FormErrors param='new_password2' errors={newPassword2Errors}/>
      </div>
      <div className="mt-4 flex gap-2 w-full">
        <button type={"submit"} className="btn btn-primary grow" disabled={response.fetching}
                onClick={() => submit()}>{hasCurrentPassword ? 'Change' : 'Set'}</button>
        <button type={"submit"} className="btn grow" disabled={response.fetching}
                onClick={() => cancel()}>Cancel</button>
      </div>
    </AuthLayout>
  )
}
