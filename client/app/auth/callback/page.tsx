'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import axios,{ AxiosError, AxiosResponse } from 'axios';
/**
 * Represents a successful response from the Spotify Auth API.
 */
interface SuccessResponse {
    message: string;
}
/**
 * Represents an error response from the Spotify Auth API.
 */
interface ErrorResponse {
    error: string;
}
/**
 * Represents a response from the Spotify Auth API,
 * which could either be a success or an error.
 */
type SpotifyAuthResponse = SuccessResponse | ErrorResponse;

/**
 * The Callback component handles the OAuth callback from Spotify.
 * 
 * executes after spotify redirects to us
 * 
 * ex: http://example.com/callback?code=1234
 */

const Callback = () => {
    // Get the Next.js router object to access query parameters.
    const router = useRouter();
  
    // Use the useEffect hook to execute logic when the component mounts or updates.
    useEffect(() => {
      // Destructure the 'code' from the query parameters.
      const { code } = router.query;
  
      // If there's a code present, proceed to validate it.
      if (code) {
        // Make a POST request to validate the authorization code.
        axios.post('http://localhost:8000/spotify/auth-code/', {
          code: code
        })
        // Handle the Axios response.
        .then((response: AxiosResponse<SpotifyAuthResponse>) => {
          // Check if the response is a success message.
          if ('message' in response.data) {
            // Navigate to the dashboard page.
            router.push('/dashboard');
          }
          // Check if the response is an error message.
          else if ('error' in response.data) {
            // Log the error for debugging.
            console.error(response.data.error);
          }
        })
        // Handle any errors that occur during the Axios request.
        .catch((error) => {
          console.error(error);
        });
      }
    // Specify router.query as the dependency for the useEffect hook.
    }, [router.query]);
  
    // Display a message while the user is being authenticated.
    return <div>Authenticating...</div>;
  };
  
  export default Callback;