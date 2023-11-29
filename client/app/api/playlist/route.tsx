import { NextResponse } from "next/server";

export async function POST(request: Request){
    const body = await request.json()
    const playlist_id = body.playlist_id
    try {
        const url = 'http://localhost:8000/stats/playlist/'+playlist_id+"/"
        const response = await fetch(url,
            {
                method: 'POST',
                cache: 'no-store',
                body: JSON.stringify({
                    "type": "wordmap"
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        const data = await response.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error("Error fetching data: ", error);
        // Handle errors here
        return new Response()
    }
}