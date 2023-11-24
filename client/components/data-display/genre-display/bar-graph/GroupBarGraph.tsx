import React from 'react';
import { Group } from '@visx/group';
import { BarGroup } from '@visx/shape';
import { AxisBottom } from '@visx/axis';
import cityTemperature, { CityTemperature } from '@visx/mock-data/lib/mocks/cityTemperature';
import { scaleBand, scaleLinear, scaleOrdinal } from '@visx/scale';
import { timeParse, timeFormat } from '@visx/vendor/d3-time-format';

export type BarGroupProps = {
  width: number;
  height: number;
  margin?: { top: number; right: number; bottom: number; left: number };
  events?: boolean;
  data: GenreData[];
};
type GenreData = { 
  playlistId: string;
  playlistName: string;
  genres: {
    [genre: string]: number;
  };
}


// type CityName = 'New York' | 'San Francisco' | 'Austin';
// styling stuff

const blue = '#aeeef8';
export const green = '#e5fd3d';
const purple = '#9caff6';
export const background = '#612efb';
// get first 8 jsons in the json array
// const data = cityTemperature.slice(0, 8);
// const parseDate = timeParse('%Y-%m-%d');
// const format = timeFormat('%b %d');
// const formatDate = (date: string) => format(parseDate(date) as Date);
// accessors
const formatName = (name:string) => {
    if (name.length > 8) {
        return name.slice(0, 8);
    } else {
        return name;
    }

}
const getName = (d: GenreData) => d.playlistName;


const defaultMargin = { top: 40, right: 0, bottom: 40, left: 0 };

export default function Example({
  width,
  height,
  events = false,
  margin = defaultMargin,
  data
}: BarGroupProps) {

  const keys = Object.keys(data[0]['genres'])
  // two scale bands the first one scales the groups of group bars
  // the second one scales the individual bars in a single group
  const playlistScale = scaleBand<string>({
    domain: data.map(getName),
    padding: 0.2,
  });
  const genreScale = scaleBand<string>({
    domain: keys,
    padding: 0.1,
  });
  // scales the height of the bars
  // iterate over every dict 
  // for every dict, iterate over the key value pairs, get the max
  // create an array of the max temp for each dict
  const frequencyScale = scaleLinear<number>({
    domain: [0, Math.max(...data.map((d) => Math.max(...keys.map((key) => Number(d['genres'][key])))))],
  });
  // maps the city names to specific colors
  const colorScale = scaleOrdinal<string, string>({
    domain: keys,
    range: [blue, green, purple],
  });

  // bounds
  const xMax = width - margin.left - margin.right;
  const yMax = height - margin.top - margin.bottom;

  // update scale output dimensions
  // in reg bar char we dont account for margin so we can set it right way
  //  here we account for it and sent it layer
  // rangeRound will round to the nearest whole pixel
  playlistScale.rangeRound([0, xMax]);
  genreScale.rangeRound([0, playlistScale.bandwidth()]);
  frequencyScale.range([yMax, 0]);

  return width < 10 ? null : (
    <svg width={width} height={height}>
      <rect x={0} y={0} width={width} height={height} fill={background} rx={14} />
      <Group top={margin.top} left={margin.left}>
        <BarGroup
          data={data}
          keys={keys}
          height={yMax}
          x0={getName}
          x0Scale={playlistScale}
          x1Scale={genreScale}
          yScale={frequencyScale}
          color={colorScale}
        >
          {(barGroups) =>
            barGroups.map((barGroup) => (
              <Group key={`bar-group-${barGroup.index}-${barGroup.x0}`} left={barGroup.x0}>
                {barGroup.bars.map((bar) => (
                  <rect
                    key={`bar-group-bar-${barGroup.index}-${bar.index}-${bar.value}-${bar.key}`}
                    x={bar.x}
                    y={bar.y}
                    width={bar.width}
                    height={bar.height}
                    fill={bar.color}
                    rx={4}
                    onClick={() => {
                      if (!events) return;
                      const { key, value } = bar;
                      alert(JSON.stringify({ key, value }));
                    }}
                  />
                ))}
              </Group>
            ))
          }
        </BarGroup>
      </Group>
      <AxisBottom
        top={yMax + margin.top}
        tickFormat={formatName}
        scale={playlistScale}
        stroke={green}
        tickStroke={green}
        hideAxisLine
        tickLabelProps={{
          fill: green,
          fontSize: 11,
          textAnchor: 'middle',
        }}
      />
    </svg>
  );
}