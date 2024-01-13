'use client'
import React from 'react';
import { Text } from '@visx/text';
import Wordcloud from '@visx/wordcloud/lib/Wordcloud';
import { scaleLog } from '@visx/scale';


interface CloudProps {
    width: number;
    height: number;
    data: { [key: string]: number }; // Add this to accept the JSON data
}

export interface WordData {
    text: string;
    value: number;
}
interface CloudWord {
    text: string;
    size: number; // Font size
    x: number; // Position on the x-axis
    y: number; // Position on the y-axis
    rotate: number; // Rotation angle
    font?: string; // Font family
    // Add any other properties that the Wordcloud component provides
  }
const colors = ['#143059', '#2F6B9A', '#82a6c2'];

// const getRotationDegree = () => Math.random() > 0.5 ? 60 : -60;
// This will now rotate words randomly between -30 and 30 degrees
const getRotationDegree = () => (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 30);


export default function GenreWordCloud({ width, height, data }: CloudProps) {
    // Convert JSON data to WordData array
    const words: WordData[] = Object.entries(data).map(([text, value]) => ({ text, value }));

    const fontScale = scaleLog({
        domain: [Math.min(...words.map(w => w.value)), Math.max(...words.map(w => w.value))],
        range: [10, 100],
    });

    const fontSizeSetter = (datum: WordData) => fontScale(datum.value);

    return (
        <div className="wordcloud">
            <Wordcloud
                words={words}
                width={width}
                height={height}
                fontSize={fontSizeSetter}
                font={'Impact'}
                padding={2}
                spiral={'archimedean'}
                rotate={getRotationDegree}
            >
                {(cloudWords) =>
                    cloudWords.map((w, i) => (
                        <Text
                            key={w.text}
                            fill={colors[i % colors.length]}
                            textAnchor={'middle'}
                            transform={`translate(${w.x}, ${w.y}) rotate(${w.rotate})`}
                            fontSize={w.size}
                            fontFamily={w.font}
                        >
                            {w.text}
                        </Text>
                    ))
                }
            </Wordcloud>
            <style jsx>{`
        .wordcloud {
          display: flex;
          flex-direction: column;
          user-select: none;
        }
        .wordcloud svg {
          margin: 1rem 0;
          cursor: pointer;
        }
      `}</style>
        </div>
    );
}
