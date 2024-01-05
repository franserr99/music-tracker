// Button.tsx
'use client';
interface ButtonProps {
    text: string;
    onClick: (event:React.MouseEvent<HTMLButtonElement>) => void|Promise<void>; 
  }
  
const Button: React.FC<ButtonProps> = ({ text, onClick }) => {
    return (
        <button type="button" onClick={onClick}>
        {text}
        </button>
    );
};
  
export default Button;
  