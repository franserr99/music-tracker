'use client'
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea, Checkbox } from '@mui/material';
import { PlaylistCardProp } from '../PlaylistDTOs';

// test this later
// sx={{
//     height: 120, // fixed height
//     width: '100%', //mmake width responsive 
//     objectFit: 'contain', // Ensures the image fits within the box, maintaining aspect ratio
//   }}
export default function PlaylistPreviewCard(prop: PlaylistCardProp) {

    return (
        <Card sx={{ maxWidth: 345, }} onClick={prop.handleOpen}>
          <CardActionArea>
            <CardMedia
              component="img"
              height="120"
              src={prop.images[0].url}
              alt=""
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                {prop.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {prop.description}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      );
}