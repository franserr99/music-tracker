import NextAuth, { AuthOptions } from "next-auth";
import SpotifyProvider from "next-auth/providers/spotify";

import { JWT } from "next-auth/jwt";
import { User, Profile, Account } from "next-auth";
import axios, { AxiosResponse } from "axios";
import { SpotifyProfile } from "next-auth/providers/spotify";
interface SuccessResponse { message: string }
interface ErrorResponse { error: string }
type SpotifyAuthResponse = SuccessResponse | ErrorResponse;
interface token_info {
  user_id: string, refreshToken: string, accessToken: string, expires_in: number

}

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
    async signIn({ account, profile, user }) {
      // console.log("profile.name:", profile?.name)
      // console.log("providerAccountID", account?.providerAccountId)
      const user_id = user.name?? profile?.name ?? account?.providerAccountId ?? ""

      // log user_id for debugging
      // console.log("the username we are using:", user_id);

      // check if user exists in backend
      const userExists = await checkUserExists(user_id);
      // test loading screen with wating
      const requestConfig: RequestInit = { method: "POST", cache: 'no-cache' }
      const response = await fetch("http://localhost:3000/api/test/wait", requestConfig)
      const data = await response.json()
      let result
      if (!userExists) {
        // if user does not exist, send tokens to backend for user creation
        return await handleNewUser(account, user_id);
        
      } else {
        return await handleExistingUser(user_id, account);
      }      
    }
  },
  pages: {
    signIn: '/login'
  }

}

// Checks if user exists in the backend
async function checkUserExists(user_id: string) {
  const response = await fetch(`http://localhost:8000/users/${user_id}`, { cache: 'no-cache' });
  return response.status !== 404;
}

// Handles new user registration
async function handleNewUser(account: Account | null, user_id:string) {
  if (account === null) { return false }
  const { access_token:accessToken, refresh_token:refreshToken, expires_at } = account as Account; 
  const expires_in = calculateExpiresIn(expires_at ?? 0);
  const { response } = await sendTokensToBackend({ user_id, refreshToken, accessToken, expires_in });

  if (!response.ok) {
    console.log("Error authenticating on BE, try again");
    return false;
  }
  return true;
}

// handles existing user sign-in
async function handleExistingUser(user_id: string, account: Account | null) {
  // check if refresh and access tokens are valid
  // if access token is not expired but refresh token is invalid in backend
  if (account === null) { return false }
  const tokenResponse = await fetch(`http://localhost:8000/users/token/${user_id}`);
  if (!tokenResponse.ok) { return await handleNewUser(account, user_id); }
  return true;
}

// send tokens to the backend
async function sendTokensToBackend({ user_id, refreshToken, accessToken, expires_in }: token_info) {
  const body = JSON.stringify({ user_id, refreshToken, accessToken, expires_in });
  console.log(body)
  const headers = { 'Content-Type': 'application/json' };
  const requestConfig: RequestInit = { body, headers, cache: 'no-cache', method: 'POST' };
  const response = await fetch("http://localhost:8000/spotify/auth-code/", requestConfig);
  const data = await response.json();

  return { response, data };
}

// calculate the duration in seconds until the token expires
function calculateExpiresIn(expires_at: number) {
  const now = Math.floor(Date.now() / 1000);
  return expires_at - now;
}

export const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };


// this was my first version, got really messy so going to break it up 
// async signIn({ account }) {
//   // might want to pull the email instead and use that as the userid
//   // then you can use their accountID for another purpose 
//   // different providers will auto-gen an id if none set by user
//   // but overtime the user might set or change their id
//   // mine was my actual username, but on a new account it was some random string
//   const user_id = account?.providerAccountId;
//   console.log(user_id)
//   // check if user exists 
//   const response = await fetch(`http://localhost:8000/users/${user_id}`, { cache: 'no-cache' });
//   const json = await response.json();
//   console.log(json)
//   const accessToken = account?.access_token;
//   const refreshToken = account?.refresh_token;
//   const sp_expires_at = account?.expires_at as number
//   const now = Math.floor(Date.now() / 1000);
//   const expires_in = sp_expires_at - now;
//   const sendTokens = async ()=>{
//     // send tokens and metadata to backend
//     // the backend handles user creation if user does not exist
//     const body = {
//       user_id: user_id, refreshToken: refreshToken,
//       accessToken: accessToken, sp_expires_in: expires_in
//     }
//     const headers = { 'Content-Type': 'application/json' }
//     const requestConfig: RequestInit = {
//       body: JSON.stringify(body),
//       headers: headers,
//       cache: 'no-cache',
//       method: 'POST'
//     }
//     const response = await fetch("http://localhost:8000/spotify/auth-code/", requestConfig);
//     const data = await response.json();
//     return {response, data}

//   }
//   // django throws 404 on generic api view resource not found
//   if (response.status === 404) {
//     if (refreshToken && accessToken && user_id) {
//       const {response, data} = await sendTokens()
//       if (!response.ok) {
//         console.log("Error authenticating on BE, try again");
//         return false;
//       }
//       // TODO: add the calls to your backend to get the data from the user
//     }
    // const requestConfig: RequestInit = { method: "POST", cache: 'no-cache' }
    // const response = await fetch("/api/test/wait", requestConfig)
    // const data = await response.json()

//     return true;  // Sign-in successful
//   } else {
//     // get access token from backend, if there is an error
//     // then you send the refresh and access tokens again 
//     const response = await fetch(`http://localhost:8000/users/token/${user_id}`)
//     if (!response.ok) {
//       const {response, data} = await sendTokens()
//       if (!response.ok) {
//         console.log("Error authenticating on BE, try again");
//         return false;
//       }
//     }

//   }
//   // Existing user
//   return true;
// }