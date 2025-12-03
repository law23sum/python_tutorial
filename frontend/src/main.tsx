import React, {useEffect, useState} from 'react'
import ReactDOM from 'react-dom/client'
import type {DataRouter} from 'react-router-dom';
import {RouterProvider} from "react-router-dom";
import './index.css'
import {Client, setup} from './lib/allauth'
import {AuthContextProvider} from './allauth_auth/AuthContext.jsx';
import {useConfig} from './allauth_auth/hooks.js';
import { createRouter } from './routes';

function RouterWrapper() {
  const [router, setRouter] = useState<DataRouter | null>(null);
  const config = useConfig();
  useEffect(() => {
    setRouter(createRouter(config));
  }, [config]);
  return router ? <RouterProvider router={router} /> : null;
}

// Configure allauth with environment variable
setup(
  Client.BROWSER,
  import.meta.env.VITE_ALLAUTH_BASE_URL,
  true
)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthContextProvider>
      <RouterWrapper />
    </AuthContextProvider>
  </React.StrictMode>,
)
