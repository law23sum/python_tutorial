import React from 'react';
import LoginPage from "../pages/Login";
import AuthenticateTOTP from "../pages/AuthenticateTOTP";
import LogoutPage from "../pages/Logout";
import SignupPage from "../pages/Signup";
import VerificationEmailSent from "../pages/VerificationEmailSent";
import VerifyEmail, { loader as verifyEmailLoader } from "../pages/VerifyEmail";
import ProviderCallback from "../pages/socialauth/ProviderCallback";
import ProviderSignup from "../pages/socialauth/ProviderSignup";
import RequestLoginCode from "../pages/RequestLoginCode";
import ConfirmLoginCode from "../pages/ConfirmLoginCode";
import RequestPasswordReset from "../pages/RequestPasswordReset";
import ConfirmPasswordResetCode from "../pages/ConfirmPasswordResetCode";
import {ResetPasswordByCode, ResetPasswordByLink, resetPasswordByLinkLoader} from "../pages/ResetPassword";
import ChangePassword from "../pages/ChangePassword";
import {AnonymousRoute, AuthenticatedRoute} from '../allauth_auth/routing';

export const authRoutes = [
  {
    path: "/account/login",
    element: <AnonymousRoute><LoginPage /></AnonymousRoute>
  },
  {
    path: "/account/login/otp",
    element: <AnonymousRoute><AuthenticateTOTP /></AnonymousRoute>,
  },
  {
    path: "/account/logout",
    element: <LogoutPage />,
  },
  {
    path: "/account/signup",
    element: <AnonymousRoute><SignupPage /></AnonymousRoute>,
  },
  {
    path: '/account/verify-email',
    element: <VerificationEmailSent />
  },
  {
    path: '/account/verify-email/:key',
    element: <VerifyEmail />,
    loader: verifyEmailLoader
  },
  {
    path: '/account/provider/callback',
    element: <ProviderCallback />
  },
  {
    path: '/account/provider/signup',
    element: <AnonymousRoute><ProviderSignup /></AnonymousRoute>
  },
  {
    path: '/account/login/code',
    element: <AnonymousRoute><RequestLoginCode /></AnonymousRoute>
  },
  {
    path: '/account/login/code/confirm',
    element: <AnonymousRoute><ConfirmLoginCode /></AnonymousRoute>
  },
  {
    path: '/account/password/reset',
    element: <AnonymousRoute><RequestPasswordReset /></AnonymousRoute>
  },
  {
    path: '/account/password/reset/confirm',
    element: <AnonymousRoute><ConfirmPasswordResetCode /></AnonymousRoute>
  },
  {
    path: '/account/password/reset/complete',
    element: <AnonymousRoute><ResetPasswordByCode /></AnonymousRoute>
  },
  {
    path: '/account/password/reset/key/:key',
    element: <AnonymousRoute><ResetPasswordByLink /></AnonymousRoute>,
    loader: resetPasswordByLinkLoader
  },
  {
    path: '/account/password/change',
    element: <AuthenticatedRoute><ChangePassword /></AuthenticatedRoute>
  },
];
