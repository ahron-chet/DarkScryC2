import NextAuth, { AuthOptions, User } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import JWT from 'jsonwebtoken';

async function GetUserDetails(accessToken:string){
  const user_id = (JWT.decode(accessToken) as { sub: string }).sub;
  const res = await fetch(`${process.env.NEXT_PUBLIC_DJANGO_API_URL_V2}/users/${user_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `bearer ${accessToken}`,
    },
  });
  return await res.json();
}

export const authOptions: AuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text"},
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials, req) {

        const res = await fetch(`${process.env.NEXT_PUBLIC_DJANGO_API_URL_V2}/auth/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: credentials?.username,
            password: credentials?.password,
          }),
        });
        if (!res.ok){
          return null;
        }
        const json_res = await res.json();
        const user_details = await GetUserDetails(json_res.token);
        if (json_res) {
          return {        
              id: user_details.user_id || "AnonUser",
              userName: credentials?.username,
              accessToken: json_res.token,
              refreshToken: json_res.refresh_token,
              first_name: user_details.first_name,
              last_name: user_details.last_name,
              email: user_details.email,
              role: user_details.role,
            };
          }
        return null;
      },
    }),
  ],
  jwt:{
    maxAge: 60 * 60 * 24 * 30,
  },
  callbacks: {
    
    async jwt({ token, user, account }) {
      console.log({ account });

      return { ...token, ...user };
    },
    async session({ session, token, user }) {
      session.user = token as any;

      return session;
    },
  },
  pages: {
    // signIn: "/login",
    // error: "/auth/error",
  },
};
const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
