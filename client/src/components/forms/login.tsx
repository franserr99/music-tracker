import { useState } from "react";
const NavBar = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isSignedIn, setIsSignedIn] = useState(isUserSignedIn());

    function isUserSignedIn(): boolean  {
        /* some function call to determined if they are signed in */
        return true;
    }
    // this would be a react hook call back function
    function handleLogout() {
        setIsModalOpen(false);
        setIsSignedIn(false);
    }
    function openSignInModal() {
        setIsModalOpen(true);

    }
    
    return (
        <nav>
            {/* common links visible to all*/}
            {isSignedIn ? (
                <div>
                    {/** links unique to being signed in */}
                    <button onClick={handleLogout}>Logout</button>
                </div>

            ) : (
                <div>
                    <button onClick={openSignInModal}>Login/SignUp</button>
                </div>
            )}
        </nav>
    );
};
export default NavBar;