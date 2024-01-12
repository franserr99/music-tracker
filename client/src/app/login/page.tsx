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
        await signIn('spotify', {callbackUrl:`/${session?.user_id}`, redirect:false})
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
        <div className="flex flex-col grow overscroll-contain items-center justify-center bg-gray-50">
            {/* here you can you put different images, etc to showcase the kind of data that you can present */}
            {showTrivia && triviaData && <LoadingScreen screens={triviaData} />}
            {session ? (
                
                <div >
                    <p className="text-xl mb-4 text-gray-700">Welcome, {session?.user?.name}</p>
                    {/** links unique to being signed in */}
                    <br />
                    <button onClick={()=>signOut()}>Logout</button>
                </div>

            ) : (!showTrivia)  ? (
                <div className="shadow-lg p-2 bg-white rounded-lg" >
                    <Button onClick={handleSignIn} text="Login with Spotify"/>
                </div>
            ): null}
        </div>
    );
}

