import { NextResponse } from "next/server";

export async function POST(request: Request){

    const body = await request.json()
    const playlist_id = body.playlist_id
    console.log("inside of api method:",playlist_id)
    try {
        const url = 'http://localhost:8000/stats/playlist/'+playlist_id+"/"
        const response = await fetch(url,
            {
                method: 'POST',
                cache: 'no-store',
                body: JSON.stringify({
                    "type": "bar-chart"
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        const data = await response.json();
        console.log(data)
        return NextResponse.json(data);

    } catch (error) {
        console.error("Error fetching data: ", error);
        // Handle errors here
        return new Response()
    }
}