import React from 'react';
import ErrorPage from "../error-page";
import Profile from "../pages/dashboard/Profile";
import EmployeeApp from "../pages/dashboard/Employees";
import Dashboard from "../pages/dashboard/Dashboard";
import {NavigationDemo, NavigationDemoRoutes} from "../pages/dashboard/NavigationDemo";

export const dashboardRoutes = [
  {
    path: "/dashboard/",
    element: <Dashboard />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/dashboard/profile",
        element: <Profile />,
      },
      {
        path: "/dashboard/navigation/",
        element: <NavigationDemo />,
        children: [
          {
            path: "*",
            element: <NavigationDemoRoutes />,
          }
        ]
      },
      {
        path: "/dashboard/employees/*",
        element: <EmployeeApp />,
      },
    ]
  }
];
