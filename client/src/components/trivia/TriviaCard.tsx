
export default function TriviaCard(props: {question:string, answer:string}){
    return <div>
        <h1>{props.question}</h1>

        <h4>{props.answer}</h4>
    </div>
    
}