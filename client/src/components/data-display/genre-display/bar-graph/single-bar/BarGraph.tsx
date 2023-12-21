'use client'
import { useMemo } from 'react';
import { Bar } from '@visx/shape';
import { Group } from '@visx/group';
import { GradientTealBlue } from '@visx/gradient';
import { scaleBand, scaleLinear } from '@visx/scale';
import { Text } from '@visx/text';

export interface BarChartProps {
  // of the bar chart, not a single bar
  width: number;
  height: number;
  // genre name is key, frequency is the value
  // this is how backend sends it
  data: { [key: string]: number };
  // enables interactive features
  events?: boolean;
}

export default function BarChart({ width, height, data, events = false }: BarChartProps) {
  // convert json to an arr of key-value pairs 
  const dataEntries = useMemo(() => Object.entries(data), [data]);
  // get an arr of the values, spread it over Math.max 
  const maxCount = useMemo(() => Math.max(...Object.values(data)), [data]);
  // define the threshold
  const threshold = maxCount * 0.1;
  // filter the dataEntries to those above the threshold
  const filteredDataEntries = useMemo(() => dataEntries.filter(
                                  ([, value]) => value >= threshold
                                  ), [dataEntries, threshold]);

  const verticalMargin = 120;

  // bounds
  const xMax = width;
  const yMax = height - verticalMargin;

  // handles scaling for the num of entities we want to visualize
  const xScale = useMemo(
    () =>
    // use a scaleBand for this
    // domain is the set of inputs (category names)
    // range is the amount of visual space alloted for the visualization
      scaleBand<string>({
        range: [0, xMax],
        round: true,
        // get key arr
        domain: filteredDataEntries.map(([key,]) => key),
        padding: 0.4,
      }),
    [xMax, filteredDataEntries],
  );
  // handles scaling for the height of each entity we want to visualize
  const yScale = useMemo(
    () =>
      scaleLinear<number>({
        // in svg, a lower y value is higher on page, so yMax is the minimum
        range: [yMax, 0],
        round: true,
        // domain is 0->max from my counts
        // needs to account visually for the max one 
        // (scale it all relative to it)
        domain: [0, Math.max(...filteredDataEntries.map(([, value]) => value))],
      }),
    [yMax, filteredDataEntries],
  );
  // if width of chart is less than 10 pixels, dont render
  return width < 10 ? null : (
    // svg element
    <svg width={width} height={height}>
      <GradientTealBlue id="teal" /> 
      {/* create a rect same dim as the svg */}
      <rect width={width} height={height} fill="url(#teal)" rx={14} />
      {/* group positions the group of bars within the svg */}
      <Group top={verticalMargin / 4}>
        {/* iterate over each filtered key/value */}
        {filteredDataEntries.map(([key, value]) => {
          {/* compute the bar width/height and the x/y coordinates for the bar */}
          const barWidth = xScale.bandwidth();
          const barHeight = yMax - (yScale(value) ?? 0);
          const barX = xScale(key);
          const barY = yMax - barHeight;
          {/* wrap in a group to contain all graphical elements */}
          return (
            <Group key={`bar-group-${key}`}>
              {/* create the bar */}
              <Bar
                x={barX}
                y={barY}
                width={barWidth}
                height={barHeight}
                fill="rgba(23, 233, 217, .5)"
                onClick={() => {
                  if (events) alert(`clicked: ${key} - ${value}`);
                }}
              />
              {/* label for the bar */}
              <Text
                x={barX! + barWidth / 2}
                y={height - (verticalMargin / 1.5 - 5)} // Adjust this value as needed
                fill="white"
                textAnchor="middle"
                verticalAnchor="end"
                transform={`rotate(-45 ${barX! + barWidth / 2} ${height - (verticalMargin / 1.5 - 10)})`}
              >
                {key}
              </Text>
            </Group>
            
          );
        })}
      </Group>
    </svg>
  );
}
