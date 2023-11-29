'use client'
import { useState } from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import FullWidthGrid from "../../../ui/Grid";
import { PlaylistCardProp, PlaylistProp, image, image_urls } from "../PlaylistDTOs"
import { RenderItemFunction } from '../../../ui/uiDTOs';
import PlaylistPreviewCard from './PlaylistPreviewCard';
import BasicModal from '../PlaylistModal';
const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));

export const PlaylistGrid: React.FC<{ playlists: PlaylistProp[], images:image_urls }> = ({ playlists, images }) => {
  const [open, setOpen] = useState(false);
  const handleOpen = (id:string) => {
    setActivePlaylistId(id);
    setOpen(true);

  }
  const handleClose = () => setOpen(false);
  const [activePlaylistId, setActivePlaylistId] = useState<string|null>(null);
  

  const renderPlaylistItem: RenderItemFunction<PlaylistProp> = (p) => (
  <Item>
    <PlaylistPreviewCard name = {p.name} id={p.id} description={p.description}
     handleOpen={()=>handleOpen(p.id)} tracks={p.tracks} images={images[p.id]} created_by={p.created_by}/>
    {activePlaylistId === p.id && <BasicModal open={open} handleClose={handleClose} playlist_id={activePlaylistId}/>}
  </Item>
  );
    return <FullWidthGrid items={playlists} renderItem={renderPlaylistItem} />;
};