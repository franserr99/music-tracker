'use client'
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import BarGraphContainer from '../genre-display/bar-graph/single-bar/BarGraphContainer';
import { ModalProps } from './PlaylistDTOs';
import { useEffect, useRef, useState, useLayoutEffect } from 'react';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '66.67vw', // 2/3 of the viewport width
  height: '50vh', // 50% of the viewport height
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  flexGrow: 1
};

export default function BasicModal({ open, handleClose, playlist_id }: ModalProps) {
  const containerRef = useRef<any>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useLayoutEffect(() => {
    console.log("open is ", open)
    console.log(containerRef.current)
    const getDimensions = () => {
      if (containerRef.current && open) {

        const newWidth = containerRef.current.offsetWidth;
        const newHeight = containerRef.current.offsetHeight;

        // Only update state if dimensions have actually changed
        if (dimensions.width !== newWidth || dimensions.height !== newHeight) {
          setDimensions({ width: newWidth, height: newHeight });
        }
      }
    }
    getDimensions()

    window.addEventListener("resize", getDimensions)
    // window.addEventListener("load", getDimensions)
    console.log("inside of useEffect")
    console.log(dimensions)
    console.log(containerRef?.current?.offsetWidth, containerRef?.current?.offsetHeight)

    return () => {
      window.removeEventListener("resize", getDimensions);
      // window.removeEventListener("load", getDimensions);
    }

  }, [open]);

  console.log(dimensions.width, dimensions.height)

  return (
    <div >
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">
        <Box sx={style} ref={containerRef}>
          {/* {dimensions.width>0 && dimensions.height>0 && <BarGraphContainer playlist_id={playlist_id} width={dimensions.width} height={dimensions.height} />} */}
          <BarGraphContainer playlist_id={playlist_id} width={dimensions.width} height={dimensions.height} />
        </Box>
      </Modal>
    </div>
  );
}