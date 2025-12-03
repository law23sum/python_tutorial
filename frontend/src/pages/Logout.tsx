import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import { logout } from "../lib/allauth.js";


export default function LogoutPage() {
  const navigate = useNavigate();
  useEffect(() => {
    logout().then((content: unknown) => {
      navigate("/")
    }).catch((e: unknown) => {
      console.error(e);
    });
  }, [navigate]);

  return null;
}
