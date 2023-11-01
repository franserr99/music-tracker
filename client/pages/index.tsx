'use client'
import Footer from '../components/layout/Footer'
import Header from '../components/layout/Header'
import Button from '../components/ui/Button'
import axios from 'axios'

const HomePage : React.FC=()=>{

    const onClick= ()=>{
        //initiate the auth code flow, provide the correct uri and 
        // it should hit the callback.tsx page
        // and that should handle the backend communication 
        console.log("button was clicked");


        var client_id = '4cbf19a57d8a45248430ffe0a199b9fd'; // Your client id
        
        //var client_secret = 'e88c052b9ae04c48b804aa7e6893c988'; // Your secret
        const redirectUri = encodeURIComponent("http://localhost:3000/auth/callback");
        const scope = encodeURIComponent("user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing streaming playlist-read-private user-read-playback-position user-top-read user-read-recently-played user-library-read");

        var generateRandomString = function(length:number) {
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
        <Footer/>
        <Button onClick={onClick} text='Authorize'/>
        <Header/>
    </div>
    );
}

export default HomePage