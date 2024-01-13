'use client'
import BarChart from "./BarGraph";
import React, { useState, useEffect, useRef } from 'react';


export default async function BarGraphContainer(props: { playlist_id: string, width:number,height:number }) {

    
    // const containerRef = useRef<any>(null);
    // const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    // useEffect(() => {
    //     if (containerRef.current) {
    //         setDimensions({
    //             width: containerRef.current.offsetWidth,
    //             height: containerRef.current.offsetHeight
    //         });
    //     }
    // }, []);
    // console.log(dimensions.width, dimensions.height)

    // Some dimensions for the word cloud
    // const width = 700;
    // const height = 500;



    const body = {
        'playlist_id': props.playlist_id
    }
    const response = await fetch('http://localhost:3000/api/playlist', {
        cache: "no-cache",
        method: "POST", body: JSON.stringify({ "playlist_id": props.playlist_id })
    })
    const jsonData = await response.json()
    // Render your component with the fetched data
    return (
        <div>
            {jsonData && <BarChart width={props.width} height={props.height} data={jsonData} />}
        </div>
    );
}