'use client'
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea, Checkbox } from '@mui/material';
import { PlaylistCardProp } from '../PlaylistDTOs';


export default function PlaylistPreviewCard(prop: PlaylistCardProp) {
  const handleCheckboxChange = (event:React.ChangeEvent<HTMLInputElement>) => {
    event.preventDefault()
    event.stopPropagation();
    prop.onSelectionChange(event.target.checked);
  };
  return (
    
    <Card sx={{ maxWidth: 345, }} >
      <CardActionArea onClick={prop.handleOpen}>
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
      <Checkbox 
        sx={{zIndex:1, position:"relative"}}
        checked={prop.isSelected}
        onChange={(event) => handleCheckboxChange(event)
        }
      />
    </Card>
  );
}