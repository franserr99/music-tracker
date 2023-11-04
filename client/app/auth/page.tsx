import Button from "../../components/ui/Button";

//var client_secret = 'e88c052b9ae04c48b804aa7e6893c988'; // Your secret
const HomePage : React.FC=()=>{

    const onClick= ()=>{
        //initiate the auth code flow, provide the correct uri and 
        //it should hit the callback.tsx page
        //and that should handle the backend communication 
        console.log("button was clicked");
        const client_id = '4cbf19a57d8a45248430ffe0a199b9fd'; // Your client id
        const redirectUri = encodeURIComponent("http://localhost:3000/auth/callback");
        const scope = encodeURIComponent("user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing streaming playlist-read-private user-read-playback-position user-top-read user-read-recently-played user-library-read");
        const generateRandomString = function(length:number) {
            var text = '';
            var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            for (var i = 0; i < length; i++) {
              text += possible.charAt(Math.floor(Math.random() * possible.length));
            }
            return text;
        };
        var state = generateRandomString(16);
        const authUrl = `https://accounts.spotify.com/authorize?response_type=code&client_id=${client_id}&scope=${scope}&redirect_uri=${redirectUri}&state=${state}`;
        // Redirect the user
        window.location.href = authUrl;
    }
    return (
    <div>
        <Button onClick={onClick} text='Authorize'/>
    </div>
    );
}

export default HomePage;