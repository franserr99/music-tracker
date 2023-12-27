'use client';
import {signIn, signOut, useSession} from 'next-auth/react'

const NavBar = () => {
    // how we get session on client components
    const sessionData = useSession()
    const {data:session} = sessionData
    if (session) {
        console.log(sessionData)
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
                    <button onClick={()=>signIn()}>Login/SignUp</button>
                </div>
            )}
        </nav>
    );
};
export default NavBar;