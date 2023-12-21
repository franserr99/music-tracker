'use client'
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import BarGraphContainer from '../genre-display/bar-graph/single-bar/BarGraphContainer';
import { ModalProps } from './PlaylistDTOs';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 750,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};



export default function BasicModal({ open, handleClose, playlist_id }: ModalProps) {
    console.log(playlist_id)

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">

        <Box sx={style}>
          <BarGraphContainer playlist_id={playlist_id}/>
        </Box>
      </Modal>
    </div>
  );
}