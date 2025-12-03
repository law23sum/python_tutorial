import { useAuthInfo } from "../../allauth_auth/hooks";
import { Link } from 'react-router-dom'


export default function Profile() {
  const { user } = useAuthInfo();
  return (
    <div className="flex items-center">
      <div className="mr-4">
        <div className="avatar">
          <div className="w-24 rounded-full">
            <img src={user?.avatar_url}/>
          </div>
        </div>
      </div>
      <div>
        <p className="font-extrabold">
          {user?.display}
        </p>
        <p>
          {user?.email}
        </p>
        <p>
          <Link className={"link"} to={"/account/password/change"}>Change Password</Link>
        </p>
      </div>
    </div>
  );
}
