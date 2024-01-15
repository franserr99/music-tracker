'use client'
import TopGenresGroupBarGraph, { GenreData } from './GroupBarGraph';

async function getData(ids: string[]) {
  try {
    const url = 'http://localhost:8000/stats/playlist/'
    const requestConfig: RequestInit = {
      method: 'POST',
      cache: 'no-store',
      body: JSON.stringify({
        "type": "different-group-bar-chart",
        "ids": ids
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    }
    const response = await fetch(url, requestConfig);
    const data = await response.json();
    return data

  } catch (error) {
    console.error("Error fetching data: ", error);
    // Handle errors here
    return null
  }
}
const processTopThreeGenres = (data: GenreData[]) => {
  return data.map(playlist => {
    const sortedGenres = Object.entries(playlist)
      .filter(([key, value]) => key !== 'playlist_id' && typeof value === 'number')
      .sort(([, a], [, b]) => Number(b) - Number(a)) // Safe to cast now, as non-numeric values are filtered out
      .slice(0, 3);

    return {
      "playlist_id": playlist.playlist_id,
      '1st': sortedGenres[0] ? sortedGenres[0][1] : '',
      '2nd': sortedGenres[1] ? sortedGenres[1][1] : '',
      '3rd': sortedGenres[2] ? sortedGenres[2][1] : ''
    };
  });
};
const mapData = (data: GenreData[]) => {
  return data.map(playlist => {
    const sortedGenres = Object.entries(playlist)
      .filter(([key, value]) => key !== 'playlist_id' && typeof value === 'number')
      .sort(([, a], [, b]) => Number(b) - Number(a)) // Safe to cast now, as non-numeric values are filtered out
      .slice(0, 3);

    return {
      "playlist_id": playlist.playlist_id,
      '1st': sortedGenres[0] ? sortedGenres[0][0] : '', // assuming you want the genre name here
      '2nd': sortedGenres[1] ? sortedGenres[1][0] : '',
      '3rd': sortedGenres[2] ? sortedGenres[2][0] : ''
    };
  });


};

export default async function TopGenresGroupBarGraphContainer(props: {ids:string[]}) {

  // Some dimensions for the word cloud
  const width = 700;
  const height = 500;
  const jsonData = await getData(props.ids)

  // Render your component with the fetched data
  return (
    <div>
      {jsonData && <TopGenresGroupBarGraph width={width} height={height} data={processTopThreeGenres(jsonData)} mappedData={mapData(jsonData)} />}
    </div>
  );
}