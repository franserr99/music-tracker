import React from 'react';
import Head from 'next/head';
import styles from '../../styles/Dashboard.module.css';
import WordCloudContainer from '../../components/data-display/genre-display/word-cloud/GenereWordCloudContainer';
import Playlist from '../../components/data-display/playlists/Playlist';
 // make sure to create the corresponding CSS module

// Dummy data for the graphs
const data = {
  sales: [50, 60, 70, 80, 90, 100],
  expenses: [30, 40, 50, 60, 70, 80]
};

const Dashboard = () => {
  return (
    <div className={styles.dashboard}>
      <Head>
        <title>Dashboard</title>
      </Head>
      <h1>Dashboard</h1>

      <Playlist/>
      

      {/* More components or graphs can be added here */}
    </div>
  );
};

export default Dashboard;
