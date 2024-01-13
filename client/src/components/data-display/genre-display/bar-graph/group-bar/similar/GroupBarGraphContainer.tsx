import GroupBarGraph from './GroupBarGraph'
async function getData() {
    try {
        const url = 'http://localhost:8000/stats/playlist/'
        const response = await fetch(url,
            {
                method: 'POST',
                cache: 'no-store',
                body: JSON.stringify({
                    "type": "similar-group-bar-chart",
                    "ids": ["3H95dINDNLwAWTthxtd9Gv", "0g9HrQt3NnQmll6WP0vuIk"]
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

export default async function SimilarGenresGroupBarGraphContainer() {

    // Some dimensions for the word cloud
    const width = 700;
    const height = 500;

    const jsonData = await getData()
    // Render your component with the fetched data
    return (
        <div>
            {jsonData && <GroupBarGraph width={width} height={height} data={jsonData} />}
        </div>
    );
}