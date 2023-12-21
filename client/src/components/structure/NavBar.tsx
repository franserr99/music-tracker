const NavBar = () => {
    const userSignedIn = {/* some function call to determined if they are signed in */ }
    // this would be a react hook call back function
    function handleLogout() {

    }
    function openSignInModal() {

    }
    return (
        <nav>
            {/* common links visible to all*/}
            {userSignedIn ? (
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