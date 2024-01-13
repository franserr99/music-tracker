import Link from 'next/link'
import Image from 'next/image'
const HomePage: React.FC = () => {

    return (
        <div className='overscroll-contain flex-grow'>
            <img className='pointer-events-none mx-auto absolute inset-0 w-full h-full object-cover opacity-40' src='/bg.png' alt='background image' />
        </div>
    );

}
export default HomePage;