import { SignIn } from '@clerk/clerk-react'

function SignInPage() {
  return (
    <div className="flex items-center justify-center min-h-screen py-12">
      <SignIn
        routing="path"
        path="/sign-in"
        fallbackRedirectUrl="/home"
        signUpUrl="/sign-up"
      />
    </div>
  );
}

export default SignInPage