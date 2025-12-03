import pegasusLogo from '/rocket-laptop.svg'
import './App.css'
import {Link} from "react-router-dom";
import { useAuthInfo } from '../allauth_auth/hooks.js';

function App() {
  const { user } = useAuthInfo();
  return (
    <>
      <div className="flex justify-center items-center h-screen m-8">
        <div className="flex flex-col gap-y-12">
          <div className="flex justify-end">
            {
              user ? (
                <div>Hi {user!.display}! <Link to="/dashboard/profile">Visit your profile</Link></div>
              ) : (
                <div className={"flex gap-x-8 justify-center"}>
                  <Link to="/account/signup">Sign Up</Link>
                  <Link to="/account/login">Login</Link>
                </div>
              )
            }
          </div>
          <div className="flex justify-center">
            <img src={pegasusLogo} className="my-8" alt="Pegasus logo"/>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Vite + React + Pegasus</h1>
          <p className="edit-guidance">
            Edit <code>src/App.tsx</code> and save to test HMR
          </p>
        </div>
      </div>
    </>
  )
}

export default App
