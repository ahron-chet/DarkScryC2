import NextAuth from "next-auth";

declare module "next-auth" {
  /**
   * Returned by `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
   */
  interface Session {
    user: {
      id: string;
      first_name: string;
      last_name: string;
      email: string;
      userName: string;
      accessToken: string;
      refreshToken: string;
      role: string;
    };
  }
}
