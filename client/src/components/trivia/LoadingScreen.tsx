'use client'

import { useEffect, useState } from "react";
import TriviaCard from "./TriviaCard";
import { QuestionAnswer } from "../uiDTOs";


export default function LoadingScreen(props:{screens:QuestionAnswer[]}) {
    const [currentScreen, setCurrentScreen] = useState(0);
    // need this to reset the cards we got
    const screens = props.screens 

    useEffect(() => {
        console.log("Current Screen: ", currentScreen);
        // reset the cards when we went over all them
        if (currentScreen > screens.length - 1) {
            setCurrentScreen(0);
        }
        // change the loading screen after 10 seconds
        const timer = setTimeout(() => {
            // update the stage to render the next screen
            setCurrentScreen(currentScreen + 1);
        }, 10000);

        return () => clearTimeout(timer);  // clear the timer if the component unmounts
    }, [currentScreen]);

    function renderCurrentScreen(){
        const qna =screens[currentScreen];
        const question = qna._id;
        const answer = qna.answer;
        return <TriviaCard question={question} answer={answer}/>

    }
    return renderCurrentScreen();
}