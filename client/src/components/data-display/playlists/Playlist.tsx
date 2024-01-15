import BarGraphContainer from "../genre-display/bar-graph/single-bar/BarGraphContainer";
// import WordCloudContiner from "../genre-display/word-cloud/GenereWordCloudContainer";
import SimilarGenresGroupBarGraphContainer from "../genre-display/bar-graph/group-bar/similar/GroupBarGraphContainer";
import TopGenresGroupBarGraphContainer from "../genre-display/bar-graph/group-bar/difference/GroupBarGraphContainer";
import PlaylistPreview from "./preview/PlaylistPreview";
import { UserProp } from "./PlaylistDTOs";
export default function Playlist(prop:UserProp) {
    return (
        <div>

            <PlaylistPreview user_id={prop.user_id}/>
            {/* <h2>
                Group Bar Chart For Genres Playlist Share In Common
            </h2>
            <SimilarGenresGroupBarGraphContainer/>
            <h2>
                Group Bar Chart For Top Genres Each One Has
            </h2>
            <TopGenresGroupBarGraphContainer/> */}
        </div >
    );

}