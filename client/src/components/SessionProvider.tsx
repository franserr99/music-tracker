'use client';

import {SessionProvider} from "next-auth/react"
// it renders the children passed to it, so we dont need to worry about 
// client server composition 
export const config = {matcher: ['/dashboard']}
export default SessionProvider;