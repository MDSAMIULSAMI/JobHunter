import { SignUp } from '@clerk/clerk-react'

function SignUpPage() {
  return (
    <div className="flex items-center justify-center min-h-screen py-12">
      <SignUp
        routing="path"
        path="/sign-up"
        fallbackRedirectUrl="/home"
        signInUrl="/sign-in"
      />
    </div>
  );
}

export default SignUpPage