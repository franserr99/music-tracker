'use client';
import {signIn, signOut, useSession} from 'next-auth/react'

const NavBar = () => {
    // how we get session on client components
    const {data:session, status} = useSession()
    if(session === undefined){
        // session has not been fetched yet
    }else if(session === null){
        // failed to retrieve session
    }else{
        // session obj
        console.log(session)
    }

    if (status === "loading"){
        // we can show trivia cards on this status
    } else if(status ==="authenticated"){
        // 
    }else {
        // statis === "unauthenticated"
    }
    return (
        <nav>
            {/* common links visible to all*/}
            {session ? (
                
                <div>
                    {/** links unique to being signed in */}
                    {session?.user?.name}
                    <br />
                    <button onClick={()=>signOut()}>Logout</button>
                </div>

            ) : (
                <div>
                    <button onClick={()=>signIn('spotify',{callbackUrl:'/dashboard'})}>Login</button>
                </div>
            )}
        </nav>
    );
};
export default NavBar;