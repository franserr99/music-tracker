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

    const handleSignIn = async () => {
        setIsProcessing(true);
        signIn('spotify', {callbackUrl:"/dashboard"})
        setIsProcessing(false);
    };
    useEffect(() => {
        // see if we should show trivia
        setShowTrivia(status === 'loading' || isProcessing);
    }, [status, isProcessing]);

    useEffect(()=>{
        const fetchData = async()=>{
            const response = await fetch("/api/trivia/qna");
            if (response.ok) {
                const data = await response.json() as QuestionAnswer[];            
                setTriviaData(data);
            }
        }
        fetchData();

    },[])


    return (
        <div>
            {showTrivia && triviaData && <LoadingScreen screens={triviaData} />}
            {/* Your login page content */}
            

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

