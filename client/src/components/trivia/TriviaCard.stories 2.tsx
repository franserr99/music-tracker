import type { Meta, StoryObj } from '@storybook/react';
import TriviaCard from './TriviaCard';
import "../../app/globals.css";
import RootLayout from '@/app/layout';
import Login from '@/app/login/page';
// const meta: Meta<typeof TriviaCard> = {
//     component: TriviaCard,
// };

// export default meta;

// type Story = StoryObj<typeof TriviaCard>;

// export const FirstStory: Story = {
//     args: {
//      question: " How many albums does Led Zeppelin have?",
//      answer: "Eight"
//     },
//   };

const meta: Meta<typeof TriviaCard> = {
    title: 'Example/TriviaCard',
    component: TriviaCard,
};

export default meta;

type Story = StoryObj<typeof TriviaCard>;

export const FirstStory: Story = {
    render: () => (
        <div className='flex flex-col min-h-screen min-w-full'>
            <div className='flex flex-col grow overscroll-contain'>
            <TriviaCard 
                    question="How many albums does Led Zeppelin have?"
                    answer="Eight"/>
            </div>
        </div>
            
    ),
};
