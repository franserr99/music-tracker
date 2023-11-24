import BarGraphContainer from "../genre-display/bar-graph/BarGraphContainer";
import WordCloudContiner from "../genre-display/word-cloud/GenereWordCloudContainer";


export default function Playlist() {
    return (
        <div>
            <WordCloudContiner />
            <BarGraphContainer/>
        </div >
    );

}