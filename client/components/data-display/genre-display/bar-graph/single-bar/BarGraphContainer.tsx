import BarChart from "./BarGraph";

async function getData() {
    try {
        const url = 'http://localhost:8000/stats/playlist/7yBjn2fb4igpGlTUdl5Kxm/'
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
        return data

    } catch (error) {
        console.error("Error fetching data: ", error);
        // Handle errors here
        return null
    }

}

export default async function BarGraphContainer() {

    // Some dimensions for the word cloud
    const width = 700;
    const height = 500;

    const jsonData = await getData()
    // Render your component with the fetched data
    return (
        <div>
            {jsonData && <BarChart width={width} height={height} data={jsonData} />}
        </div>
    );
}