'use client'
import BarChart from "./BarGraph";


export default async function BarGraphContainer(props: {playlist_id:string}) {
    console.log(props.playlist_id)

    // Some dimensions for the word cloud
    const width = 700;
    const height = 500;
    
    const body= {
        'playlist_id':props.playlist_id
    }
    const response = await fetch('http://localhost:3000/api/playlist', { cache:"no-cache",
        method:"POST",body: JSON.stringify({"playlist_id":props.playlist_id})
    })
    const jsonData = await response.json()
    // Render your component with the fetched data
    return (
        <div>
            {jsonData && <BarChart width={width} height={height} data={jsonData} />}
        </div>
    );
}