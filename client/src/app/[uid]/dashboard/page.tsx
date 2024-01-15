import React from 'react';
import Head from 'next/head';

import Playlist from '../../../components/data-display/playlists/Playlist';

interface PageProps {
  params: {
    uid: string;
  };
}
const Page = ({ params }: PageProps) => {
  

  return (
    <div className='grow'>
      <Head>
        <title>Dashboard</title>
      </Head>

      <h1 className='mb-5 text-center'>Dashboard</h1>

      <Playlist user_id={params.uid}/>
      
      {/* More components or graphs can be added here */}
    </div>
  );
};

export default Page;
