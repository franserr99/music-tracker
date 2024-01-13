'use client'
import {useState}  from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';

import { GenericGridProps } from '../uiDTOs';

export default function FullWidthGrid<T,>({ items, renderItem }: GenericGridProps<T>) {
  const initialItemCount = 6; // only show 6 at the start
  const [displayedItems, setDisplayedItems] = useState(initialItemCount);

  // switch between expanded and shortened
  const toggleItemsView = () => {
    if (displayedItems === initialItemCount) {
      setDisplayedItems(items.length); // show them all 
    } else {
      setDisplayedItems(initialItemCount); // shortned amount
    }
  };

  // button text depending on if they have expanded or not
  const buttonText = displayedItems === initialItemCount ? 'See More' : 'Show Less';

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        {items.slice(0, displayedItems).map((item, index) => (
          <Grid item xs={6} md={4} key={index}>
            {renderItem(item)}
          </Grid>
        ))}
      </Grid>
      {items.length > initialItemCount && (
        <Button onClick={toggleItemsView}>{buttonText}</Button> // Toggle button
      )}
    </Box>
  );
}