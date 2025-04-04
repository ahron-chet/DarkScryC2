// middleware.js
import { withAuth } from "next-auth/middleware";

export default withAuth(
  {
    pages: {
      signIn: "/login",
    },
  }
);

// By default, this protects all routes except static files, next internal routes, etc.
// Adjust the matcher to your preference.
export const config = {
  matcher: ["/((?!_next|.*\\..*|favicon.ico|login).*)"],
};
