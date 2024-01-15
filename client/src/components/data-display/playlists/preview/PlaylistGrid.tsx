'use client'
import { useState } from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import FullWidthGrid from "../../../layout/Grid";
import { PlaylistCardProp, PlaylistProp, image, image_urls } from "../PlaylistDTOs"
import { RenderItemFunction } from '../../../uiDTOs';
import PlaylistPreviewCard from './PlaylistPreviewCard';
import BasicModal from '../PlaylistModal';
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
  justifyContent: "center",
  display: "flex",
}));

export const PlaylistGrid: React.FC<{ playlists: PlaylistProp[], images: image_urls }> = ({ playlists, images }) => {
  // these states are handling the modal that opens for an individual card
  const [open, setOpen] = useState(false);
  const [activePlaylistId, setActivePlaylistId] = useState<string | null>(null);
  const [activePlaylistName, setActivePlaylistName] = useState<string | null>(null);
  // handles the modal opening for two playlists 
  const [selectedPlaylists, setSelectedPlaylists] = useState<String[]>([]);
  const handleSelectionChange = (id: string) => {
    setSelectedPlaylists(prev => {
      if(prev.includes(id)){
        return prev.filter(selected=>selected!=id);
      }else { 
        return [...prev,id]
      }
    }) 
    console.log(selectedPlaylists)
  }
  // these two functions are used to lift modal state up from the child
  const handleOpen = (id: string, name: string) => {
    setActivePlaylistId(id);
    setOpen(true);
    setActivePlaylistName(name);
  }
  const handleClose = () => setOpen(false);
  // grid will call for each item
  const renderPlaylistItem: RenderItemFunction<PlaylistProp> = (p) => (
    <Item>
      <PlaylistPreviewCard
        name={p.name}
        id={p.id}
        description={p.description}
        handleOpen={() => handleOpen(p.id, p.name)}
        tracks={p.tracks}
        images={images[p.id]}
        created_by={p.created_by}
        onSelectionChange={()=> handleSelectionChange(p.id)}
        isSelected={selectedPlaylists.includes(p.id)}
      />
      {activePlaylistId === p.id && activePlaylistName == p.name && 
          <BasicModal 
            open={open} 
            handleClose={handleClose} 
            playlist_id={activePlaylistId} 
            name={activePlaylistName} />
          }
    </Item>
  );
  return <FullWidthGrid items={playlists} renderItem={renderPlaylistItem} />;
};