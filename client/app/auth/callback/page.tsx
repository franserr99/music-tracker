'use client';

import { useEffect } from 'react';
import { useSearchParams,useRouter } from 'next/navigation';
import axios,{ AxiosError, AxiosResponse } from 'axios';

interface SuccessResponse {message: string}
interface ErrorResponse {error: string}
type SpotifyAuthResponse = SuccessResponse | ErrorResponse;



const Callback = () => {
    //i think the router is more about navigation rather than the path
    //they created new methods for the paths. not the same as for the page directory i was used to
    // const router = useRouter();
    const searchParams=useSearchParams();
    const router=useRouter();
    useEffect(() => {
      const code=searchParams.get('code')
      // if it exists, process it
      if (code) {
        // backend expects a post
        axios.post('http://localhost:8000/spotify/auth-code/', {
          code: code
        }).then((response: AxiosResponse<SpotifyAuthResponse>) => {
          //was a success
          if ('message' in response.data) {
            //go to dashboard
            router.push('/dashboard');
          }
          // failed, log the error
          else if ('error' in response.data) {
            // Log the error for debugging.
            console.error(response.data.error);
            router.push('/dashboard');
          }
        })
        // errors during request itself
        .catch((error) => {
          console.error(error);
          router.push('/dashboard');
        });
      }
    // execute when the query object changes
    }, [searchParams]);
  
    // let user know we are authenticating for now
    return <div>Authenticating...</div>;
  };
  
  export default Callback;