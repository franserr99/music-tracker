'use client'
import { signIn, signOut, useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import Button from "@/components/controls/Button";
import LoadingScreen from "@/components/trivia/LoadingScreen";



import { QuestionAnswer } from "@/components/uiDTOs";


export default function Login() {
    const { status,data:session } = useSession();
    const [isProcessing, setIsProcessing] = useState(false);
    const [showTrivia, setShowTrivia] = useState(false);
    const [triviaData , setTriviaData]= useState<QuestionAnswer[]|null>(null);
    // helper functions
    const handleSignIn = async (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault()
        setIsProcessing(true);
        await signIn('spotify', {callbackUrl:"/", redirect:false})
    };
    const fetchData = async()=>{
        const response = await fetch("/api/trivia/qna");
        if (response.ok) {
            const data = await response.json() as QuestionAnswer[];            
            setTriviaData(data);
        }
    }
    
    useEffect(() => {
        // see if we should show trivia
        setShowTrivia((status === 'loading') || isProcessing);
    }, [status, isProcessing]);
    
    useEffect(()=> { 
        fetchData();
        return () => {
            // reset processing state on unmount
            setIsProcessing(false); 
        };
     },[])


    return (
        <div>
            {showTrivia && triviaData && <LoadingScreen screens={triviaData} />}

            {session ? (
                
                <div>
                    {/** links unique to being signed in */}
                    {session?.user?.name}
                    <br />
                    <button onClick={()=>signOut()}>Logout</button>
                </div>

            ) : (
                <div>
                    <Button onClick={handleSignIn} text="Login"/>
                </div>
            )}
            
        </div>
    );
}

