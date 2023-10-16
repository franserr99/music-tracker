import { useEffect } from 'react';
import { useRouter } from 'next/router';
import axios,{ AxiosError, AxiosResponse } from 'axios';

// define the expected shape of the response
interface ApiResponse {
    // dataField1: string;
    // dataField2: number;
}
//executes after spotify redirects to us
// ex: http://example.com/callback?code=1234
const Callback: React.FC = () => {
    const router = useRouter();
  
    useEffect(() => {
        //type casting to ensure code is a string.
        const code = router.query.code as string | undefined;
  
        if (code) {
            //send to backend
            axios.post<ApiResponse>('http://localhost:8000/', {
            code: code
            })
            .then((response: AxiosResponse<ApiResponse>) => {
                //handle response
                //for now send back to dashboard, but maybe store?
                //need to think about this some more
                router.push('/dashboard');
            })
            .catch((error: AxiosError) => {
                // Handle errors.
                console.error(error);
            });
        }
    }, [router.query]);
  
    return <div>Authenticating...</div>;
  };
  
  export default Callback;