
import pandas as pd
import spotipy
from typing import Any, Dict, List
scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def partition_track_ids(track_ids: pd.Series,
                        chunk_size: int = 100) -> List[List[str]]:
    """Break track IDs into chunks of a specified size."""
    return [track_ids[i:i + chunk_size]
            for i in range(0, len(track_ids), chunk_size)]


def get_audio_features_for_tracks(client: spotipy.Spotify,
                                  track_id_chunks: List[List[str]]
                                  ) -> List[Dict[str, Any]]:
    """Fetch audio features for each chunk of track IDs."""
    all_features = []
    for chunk in track_id_chunks:
        chunk_features = client.audio_features(chunk)
        if chunk_features:
            all_features.extend(chunk_features)
    return all_features


def clean_audio_features(features: List[Dict[str, Any]]
                         ) -> List[Dict[str, Any]]:
    """Remove None entries from the list of features."""
    return [feature for feature in features if feature is not None]


def extract_features(features: List[Dict[str, Any]],
                     feature_keys: List[str]) -> List[List[Any]]:
    """Extract specified audio features from the feature data."""
    return [[feature[key] for key in feature_keys] for feature in features]


def create_audio_feature_df(parent_df: pd.DataFrame,
                            features: List[List[Any]],
                            feature_keys: List[str]) -> pd.DataFrame:
    """Create a DataFrame from audio features
    and merge with the parent DataFrame."""
    features_df = pd.DataFrame(features, columns=feature_keys)
    features_df.dropna(inplace=True)
    features_df.reset_index(drop=True, inplace=True)
    # Merge with the parent dataframe
    complete_df = pd.concat([parent_df, features_df], axis=1)
    complete_df.reset_index(drop=True, inplace=True)
    return complete_df


def get_audio_feature_df(client: spotipy.Spotify,
                         parent_df: pd.DataFrame) -> pd.DataFrame:
    """Main function to get audio feature DataFrame."""
    print(parent_df)
    parent_df.reset_index(inplace=True, drop=True)
    track_ids = parent_df['id'][:]

    # Prepare data: break into 100 item chunks
    track_id_chunks = partition_track_ids(track_ids)

    # Fetch and clean audio features
    raw_features = get_audio_features_for_tracks(client, track_id_chunks)
    clean_features = clean_audio_features(raw_features)

    # Get numerical data and extract features
    if clean_features:
        feature_column_names = list(clean_features[0].keys())[:-7]
        songs_audio_features = extract_features(
            clean_features, feature_column_names)

        # Drop tracks that do not have audio features
        eligible_parents = parent_df[~parent_df['id'].isin(
            [f['id'] for f in raw_features if f is None])]
        eligible_parents.dropna(inplace=True)
        eligible_parents.reset_index(drop=True, inplace=True)

        # Check if the tracks and features align
        assert len(eligible_parents['id']) == len(
            songs_audio_features), "Tracks were not dropped correctly."

        # Create the complete DataFrame
        return create_audio_feature_df(eligible_parents,
                                       songs_audio_features,
                                       feature_column_names)
    else:
        # Return an empty DataFrame or raise an error as appropriate
        return pd.DataFrame()


# def get_audio_feature_df(client: spotipy.Spotify, parent_df: pd.DataFrame):
#     print(parent_df)
#     parent_df.reset_index(inplace=True, drop=True)
#     partitioned_list = []
#     trackIDX = parent_df['id'][:]
#     # prep data: break into 100 item chunks
#     for i in range(0, len(trackIDX), 100):
#         partitioned_list.append(trackIDX[i:i+100])
#     all_features = dict(client.audio_features(partitioned_list[0])[0])
#     # print(all_features.keys())
#     # get numerical data
#     feature_column_names = list(all_features.keys())[:-7]
#     # keep a copy to make sure data lines up later
#     # feature_column_names.append('id')
#     songs_audio_features = []
#     # account for songs that dont have audio features
#     all_bad_indices = []
#     # iterate in chunks
#     for k, chunk in enumerate(partitioned_list):
#         features = list(client.audio_features(chunk))
#         assert (len(features) == len(chunk))
#         # clean up data
#         if None in features:
#             bad_indices = []
#             # get indicies of null values
#             for i, v in enumerate(features):
#                 if (v is None):
#                     # account for the partioning
#                     all_bad_indices.append(int(i+((k)*100)))
#                     bad_indices.append(i)
#             # get rid of items in feature list that are null
#             for j in range(len(bad_indices)):
#                 features.pop(bad_indices[j])
#         # removed all nulls by now, dealing with only a list of dictionaries
#         for song_features in features:
#             feats = []
#             for column_name in feature_column_names:
#                 feats.append(song_features[column_name])
#             songs_audio_features.append(feats)
#     eligible_parents = parent_df.drop(index=all_bad_indices)
#     eligible_parents.dropna(inplace=True)
#     eligible_parents.reset_index(inplace=True, drop=True)
#     assert (len(eligible_parents['id'][:]) == len(
#         songs_audio_features)), "tracks were not dropped correctly somewhere"
#     features_df = pd.DataFrame(
#         songs_audio_features, columns=feature_column_names)
#     features_df.dropna(inplace=True)
#     features_df.reset_index(drop=True, inplace=True)
#     complete_df = pd.concat([eligible_parents, features_df], axis=1)
#     complete_df.reset_index(inplace=True, drop=True)
#     return complete_df
