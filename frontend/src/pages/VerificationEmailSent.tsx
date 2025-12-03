import { URLs } from "../allauth_auth";
import AuthLayout from "../layouts/AuthLayout";

export default function VerificationEmailSent () {
  return (
    <AuthLayout title="Confirm Email Address">
      <p className="text-gray-600 my-8">
        Please confirm your email address by clicking the link we just sent you. Or{' '}
        <a href={URLs.LOGOUT_URL} className="pg-link">
          try starting over
        </a>.
      </p>
    </AuthLayout>
  )
}
