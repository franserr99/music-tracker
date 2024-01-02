import PlaylistPreviewCard from "./PlaylistPreviewCard";
import { PlaylistProp, image, image_urls, UserProp } from "../PlaylistDTOs"
import { PlaylistGrid } from "./PlaylistGrid";
import { getServerSession } from "next-auth";
const getPlaylistIDs = async (user_id: string) => {
    const url = 'http://localhost:8000/playlist?user_id=' + user_id
    const response = await fetch(url);
    const data = await response.json() as PlaylistProp[];
    return data
}


async function getImages(playlist_ids: string[], token: string) {
    const image_urls = {} as image_urls
    await Promise.all(playlist_ids.map(async (id) => {
        const url = 'https://api.spotify.com/v1/playlists/' + id + '/images'
        const headers = {
            'Authorization': 'Bearer ' + token
        }
        const response = await fetch(url, { headers: headers, cache: 'no-cache' });
        const image_jsons = await response.json() as image[];
        image_jsons.forEach((image) => {
            if (!(id in image_urls)) {
                image_urls[id] = [] as image[]
            }
            image_urls[id].push({ url: image.url, height: image.height, width: image.width })
        })
    }))
    return image_urls
}

export default async function PlaylistPreview(prop: UserProp) {
    const session = await getServerSession()

    // need a prop
    const playlists = await getPlaylistIDs(session?.user_id);
    const response = await fetch("http://localhost:8000/users/token/" + prop.user_id, { cache: 'no-cache' });
    const accessToken = await response.json();
    const playlist_ids = playlists.map((playlist) => playlist.id)
    const image_urls = await getImages(playlist_ids, accessToken)

    return (
        <div>
            {playlists && image_urls && <PlaylistGrid playlists={playlists} images={image_urls} />}
        </div >
    );

}