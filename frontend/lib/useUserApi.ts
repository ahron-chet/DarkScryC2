import useAxiosAuth from "lib/hooks/useAxiosAuth";

// Define the shape of the user according to your schema
export interface IUser {
  user_id?: string;
  username?: string;
  password?: string;      // Only used for updating the password
  email?: string;
  role?: string;
  first_name?: string;
  last_name?: string;
  company_name?: string;
  industry?: string;
  country?: string;
}

export default function useUserApi() {
  const axiosAuth = useAxiosAuth();

  // GET a single user by user_id
  const getUser = async (userId: string): Promise<IUser> => {
    const response = await axiosAuth.get<IUser>(`/users/${userId}`);
    return response.data;
  };

  // UPDATE (PUT) user by user_id
  // Include `password` only if you want to change it
  const updateUser = async (userId: string, updates: Partial<IUser>): Promise<IUser> => {
    const response = await axiosAuth.put<IUser>(`/users/${userId}`, updates);
    return response.data;
  };

  // Example: Create user (if needed)
  const createUser = async (userData: IUser): Promise<IUser> => {
    const response = await axiosAuth.post<IUser>("/users/", userData);
    return response.data;
  };

  // Example: Delete user (if needed)
  const deleteUser = async (userId: string): Promise<{ success: boolean }> => {
    const response = await axiosAuth.delete<IUser>(`/users/${userId}`);
    return { success: response.status === 201 };
  };

  // Example: List all users (if needed)
  const listUsers = async (): Promise<IUser[]> => {
    const response = await axiosAuth.get<IUser[]>(`/users/`);
    return response.data;
  };

  return {
    getUser,
    updateUser,
    createUser,
    deleteUser,
    listUsers,
  };
}
