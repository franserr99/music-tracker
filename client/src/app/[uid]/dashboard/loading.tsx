'use client'
import React from 'react'

import { ImSpinner9 } from "react-icons/im";
import { TailSpin } from "react-loader-spinner";

const Loading = () => {

  // console.log("loading again")
  return (
    <div className='min-h-screen'>
      <div className='flex grow justify-center align-center'>
        <TailSpin />
      </div>

    </div>

  );
}

export default Loading;