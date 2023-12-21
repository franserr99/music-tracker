export interface UserProp {
    user_id: string
}
export type image_urls = {
    [key: string]: image[];
}
export interface PlaylistProp { 
    id: string;
    tracks : string[];
    name : string;
    description: string;
    created_by:string;
    images: image[]
}
export type image = { 
    url:string;
    height: number;
    width:number;
}
export type handleCloseFunction = () =>void;
export type ModalProps = { 
    open: boolean;
    handleClose: handleCloseFunction;
    playlist_id:string;
}
export type handleOpenFunction = () =>void;

export interface PlaylistCardProp extends PlaylistProp { 
    handleOpen: handleOpenFunction
}