
import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";
import { AuthGetApi } from "@/lib/fetchApi";
import LogoutButton from "@/components/LogoutButton";
import Sidebar from "@/components/Sidebar";

export default async function HomePage() {
  const session = await getServerSession(authOptions);
  console.log(session);
  return (
    <div>
      <Sidebar />
    
      <h1>Welcome to the Home Page</h1>
      {session ? (
        <>
          <p>User ID: {session.user?.id}</p>
          <p>Username: {session.user?.userName}</p>
          <LogoutButton /> {}
        </>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
}