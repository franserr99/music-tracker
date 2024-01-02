import NextAuth, { AuthOptions } from "next-auth";
import SpotifyProvider from "next-auth/providers/spotify";

import { JWT } from "next-auth/jwt";
import { User, Profile, Account } from "next-auth";
import axios, { AxiosResponse } from "axios";

interface SuccessResponse { message: string }
interface ErrorResponse { error: string }
type SpotifyAuthResponse = SuccessResponse | ErrorResponse;

export const authOptions: AuthOptions = {
  providers: [
    SpotifyProvider({
      clientId: process.env.SPOTIFY_CLIENT_ID ?? "",
      clientSecret: process.env.SPOTIFY_CLIENT_SECRET ?? "",
      authorization: { params: { scope: process.env.SPOTIFY_SCOPE ?? "" } }
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        // add more fields to the jwt 
        const accessToken = account.access_token;
        const refreshToken = account.refresh_token;
        const user_id = account.providerAccountId;
        token.sp_accessToken = accessToken as string;
        token.sp_refreshToken = refreshToken as string;
        token.user_id = user_id
        const sp_expires_at = account.expires_at as number
        const now = Math.floor(Date.now() / 1000);
        // calculate the duration in seconds until the token expires
        const expires_in = sp_expires_at - now;
        token.sp_expires_in = expires_in;

      }
      return token;
    },
    async session({ session, token }) {
      // send properties to the client, 
      // like an access_token and user id from a provider.
      session.accessToken = token.sp_accessToken as string
      session.refreshToken = token.sp_refreshToken as string
      session.user_id = token.user_id as string
      session.sp_expires_in = token.sp_expires_in as number
      return session
    },
    async signIn({ account }) {
      // might want to pull the email instead and use that as the userid
      // then you can use their accountID for another purpose 
      // different providers will auto-gen an id if none set by user
      // but overtime the user might set or change their id
      // mine was my actual username, but on a new account it was some random string
      const user_id = account?.providerAccountId;
      console.log(user_id)
      // check if user exists 
      const response = await fetch(`http://localhost:8000/users/${user_id}`, { cache: 'no-cache' });
      const json = await response.json();
      console.log(json)
      // django throws 404 on generic api view resource not found
      if (response.status === 404) {
        // send tokens and metadata to backend
        // the backend handles user creation if user does not exist
        const accessToken = account?.access_token;
        const refreshToken = account?.refresh_token;
        const sp_expires_at = account?.expires_at as number
        const now = Math.floor(Date.now() / 1000);
        // calculate the duration in seconds until the token expires
        const expires_in = sp_expires_at - now;

        if (refreshToken && accessToken && user_id) {
          // backend expects a post
          const body = {
            user_id: user_id, refreshToken: refreshToken,
            accessToken: accessToken, sp_expires_in: expires_in
          }
          const headers = { 'Content-Type': 'application/json' }
          const requestConfig: RequestInit = {
            body: JSON.stringify(body),
            headers: headers,
            cache: 'no-cache',
            method: 'POST'
          }
          const response = await fetch("http://localhost:8000/spotify/auth-code/", requestConfig);
          const data = await response.json();
          if (!response.ok) {
            console.log("Error authenticating on BE, try again");
            return false;
          }
          // TODO: add the calls to your backend to get the data from the user
          // this is where they are going to be waiting 
          // for now, we are going to add a route that makes the user wait a set amount of time 

        }
        const requestConfig :RequestInit = {
          method:"POST", cache:'no-cache'
        }
        const response = await fetch("/api/test/wait",requestConfig)
        const data =  await response.json()

        return true;  // Sign-in successful
      }
      // Existing user
      return true;
    }

  },
  pages:{
    signIn:'/login'
  }

}

export const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };