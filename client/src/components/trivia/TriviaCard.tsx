
export default function TriviaCard(props: { question: string, answer: string }) {
    return (
        
        <div className="flex flex-col grow min-w-full p-4">
            <div className="flex flex-col flex-grow bg-gradient-to-r from-[#cfd9df] to-[#e2ebf0] justify-around shadow-lg rounded-xl p-6 text-center">
                <h1 className="text-black text-3xl font-semibold -mb-40">{props.question}</h1>
                <h4 className="text-black text-3xl font-semibold">{props.answer}</h4>
            </div>
        </div>
    );
}