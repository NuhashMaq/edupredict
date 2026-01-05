export type UserRole = "admin" | "teacher" | "student";

export type UserPublicAdmin = {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
};

export type UsersList = {
  items: UserPublicAdmin[];
  total: number;
};
