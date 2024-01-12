// Button.tsx
'use client';
interface ButtonProps {
    text: string;
    onClick: (event:React.MouseEvent<HTMLButtonElement>) => void|Promise<void>; 
  }
  
const Button: React.FC<ButtonProps> = ({ text, onClick }) => {
    return (
        <button className="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded hover:bg-gray-400 transition duration-300" type="button" onClick={onClick}>
        {text}
        </button>
    );
};
  
export default Button;
  