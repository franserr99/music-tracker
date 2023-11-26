import BarGraphContainer from "../genre-display/bar-graph/single-bar/BarGraphContainer";
import WordCloudContiner from "../genre-display/word-cloud/GenereWordCloudContainer";
import SimilarGenresGroupBarGraphContainer from "../genre-display/bar-graph/group-bar/similar/GroupBarGraphContainer";
import TopGenresGroupBarGraphContainer from "../genre-display/bar-graph/group-bar/difference/GroupBarGraphContainer";

export default function Playlist() {
    return (
        <div>
            <h2>
                Bar Chart For Playlist Genre Frequency
            </h2>
            <BarGraphContainer/>
            <h2>
                Group Bar Chart For Genres Playlist Share In Common
            </h2>
            <SimilarGenresGroupBarGraphContainer/>
            <h2>
                Group Bar Chart For Top Genres Each One Has
            </h2>
            <TopGenresGroupBarGraphContainer/>

        </div >
    );

}