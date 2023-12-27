import NextAuth from "next-auth";
import { JWT } from "next-auth/jwt";

declare module "next-auth" {
  /**
   * Extend the User model
   */
  interface User {
    id: string;
  }

  /**
   * Extend the Session model
   */
  interface Session {
    accessToken?: string;
    refreshToken?: string;
    user_id: string;
    sp_expires_in: number;
    newUser:boolean;
  }
}

declare module "next-auth/jwt" {
  /**
   * Extend the JWT model
   */
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    user_id: string;
    sp_expires_in: number;
    newUser:boolean;
  }
}
