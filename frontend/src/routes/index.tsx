import React from 'react';
import { createBrowserRouter } from "react-router-dom";
import App from '../pages/App';
import ErrorPage from "../error-page";
import Root from '../pages/Root';
import { AuthChangeRedirector } from '../allauth_auth/routing';
import { authRoutes } from './auth.routes';
import { dashboardRoutes } from './dashboard.routes';

export function createRouter(config: unknown) {
  return createBrowserRouter([
    {
      path: "/",
      element: <AuthChangeRedirector><Root /></AuthChangeRedirector>,
      errorElement: <ErrorPage />,
      children: [
        {
          path: "/",
          element: <App />,
        },
        ...authRoutes,
        ...dashboardRoutes,
      ]
    },
  ]);
}
