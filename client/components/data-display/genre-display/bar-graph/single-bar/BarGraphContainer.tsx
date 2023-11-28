'use client'
import BarChart from "./BarGraph";


export default async function BarGraphContainer(props: {playlist_id:string}) {

    // Some dimensions for the word cloud
    const width = 700;
    const height = 500;
    
    const body= {
        'playlist_id':props.playlist_id
    }
    const response = await fetch('/api/playlist', {
        method:"POST","cache":"no-cache",body: JSON.stringify({"playlist_id":props.playlist_id})
    })
    const jsonData = await response.json()
    // Render your component with the fetched data
    return (
        <div>
            {jsonData && <BarChart width={width} height={height} data={jsonData} />}
        </div>
    );
}