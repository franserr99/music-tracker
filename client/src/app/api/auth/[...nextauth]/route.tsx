import NextAuth, { AuthOptions } from "next-auth";
import SpotifyProvider from "next-auth/providers/spotify";

import { JWT } from "next-auth/jwt";
import { User, Profile, Account } from "next-auth";
import axios, { AxiosResponse } from "axios";

interface SuccessResponse {message: string}
interface ErrorResponse {error: string}
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
        async jwt({ token, user, account, profile }) {
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
        async session({ session, token, user }) {
            // Send properties to the client, 
            // like an access_token and user id from a provider.
            session.accessToken = token.sp_accessToken as string
            session.refreshToken = token.sp_refreshToken as string
            session.user_id = token.user_id as string
            session.sp_expires_in = token.sp_expires_in as number
            return session
        },
        async signIn({ user, account, profile }) {
            const user_id = account?.providerAccountId;
            console.log(user_id)

            // check if user exists 
            const response = await fetch(`http://localhost:8000/users/${user_id}`);
            const json = await response.json();
            console.log(json)

            if (json?.detail === "Not found.") {

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
                    axios.post('http://localhost:8000/spotify/auth-code/', {
                      user_id:user_id, refreshToken :refreshToken, accessToken:accessToken, sp_expires_in:expires_in
                    }).then((response: AxiosResponse<SpotifyAuthResponse>) => {
                      //was a success
                      if ('message' in response.data) {
                        //go to dashboard
                        // router.push('/dashboard');
                        console.log(response.data)
                      }
                      // failed, log the error
                      else if ('error' in response.data) {
                        // Log the error for debugging.
                        console.error(response.data.error);
                        // router.push('/dashboard');
                      }
                    })
                    // errors during request itself
                    .catch((error:any) => {
                      console.error(error);
                    //   router.push('/dashboard');
                    });
                  }
                return true;  // Sign-in successful
            }
            // Existing user
            return true;
        }

    }

}

export const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };