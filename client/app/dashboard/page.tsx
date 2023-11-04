import React from 'react';
import Head from 'next/head';
import styles from '../../styles/Dashboard.module.css';
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

      {/* Dummy graph for Sales */}
      <div className={styles.graph}>
        <h2>Sales Over Time</h2>
        <ul>
          {data.sales.map((sale, index) => (
            <li key={index}>{sale}</li>
          ))}
        </ul>
      </div>

      {/* Dummy graph for Expenses */}
      <div className={styles.graph}>
        <h2>Expenses Over Time</h2>
        <ul>
          {data.expenses.map((expense, index) => (
            <li key={index}>{expense}</li>
          ))}
        </ul>
      </div>

      {/* More components or graphs can be added here */}
    </div>
  );
};

export default Dashboard;
