import Link from 'next/link'
import Image from 'next/image'
const HomePage: React.FC = () => { 

    return ( 
        <div className='overscroll-contain flex-grow relative'> 
            <img className='mx-auto absolute inset-0 w-full h-full object-cover opacity-40' src='/bg.png' alt='background image'/>
            <div className='text-center relative z-10 p-4'>
                <Link href='/auth'> Authenticate </Link>
            </div>
            
        </div>
    );

}
export default HomePage;