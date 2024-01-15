'use client';
import { signOut, useSession } from 'next-auth/react'
import { useState } from 'react';
import { CiMenuBurger } from "react-icons/ci";
import { IoMenu } from "react-icons/io5";
import { HiMiniXMark } from "react-icons/hi2";

const Header = () => {
  const { data: session, status } = useSession()
  const [isClicked, setClicked] = useState(false);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
    setClicked(true);
  };
  const handleUnclick = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
    setClicked(false);
  };


  return (
    <div className="grid grid-cols-3 mt-3">
      <div>
        {/** empty column, need it to center site name */}
      </div>

      <div className='justify-self-center'>
        <h1 >Music Tracker</h1>
      </div>

      {
        session ? (
          <div className='justify-self-end'>
            {/** links unique to being signed in */}
            {isClicked ? (
              <div className='flex align-center'>
                <button onClick={handleUnclick} >
                  <HiMiniXMark size="1.5em" />
                </button>
                <button onClick={() => signOut()}>Logout</button>
                <br />

              </div>
            ) : (
              <div>
                <button onClick={handleClick}>
                  <IoMenu size="1.5em" />
                </button>
              </div>
            )
            }
          </div>
        ) : (
          <div>
            {/* <button onClick={()=>signIn('spotify',{callbackUrl:'/dashboard'})}>Login</button> */}
          </div>
        )
      }
    </div>
  );
};
export default Header;


