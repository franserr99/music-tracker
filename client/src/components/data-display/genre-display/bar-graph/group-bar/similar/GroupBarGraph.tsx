'use client'
import { useState, MouseEvent } from 'react';
import { Group } from '@visx/group';
import { BarGroup } from '@visx/shape';
import { AxisBottom } from '@visx/axis';
import { scaleBand, scaleLinear, scaleOrdinal } from '@visx/scale';

// used to show common genres across different playlists
export type BarGroupProps = {
  width: number;
  height: number;
  margin?: { top: number; right: number; bottom: number; left: number };
  events?: boolean;
  data: GenreData[];
};
type BarInfo = {
  key : string;
}
type GenreData = { 
  playlist_id: string;
  [key: string]: number | string; 
}
// styling stuff
const blue = '#aeeef8';
export const green = '#e5fd3d';
const purple = '#9caff6';
export const background = '#612efb';

const getID = (d: GenreData) => String(d.playlist_id);
const defaultMargin = { top: 40, right: 0, bottom: 40, left: 0 };
 
export default function SimilarGenresGroupBarGraph({
  width,
  height,
  events = false,
  margin = defaultMargin,
  data
}: BarGroupProps) {
  // hook to handle the hover information 
  const [hoverInfo, setHoverInfo] = useState({key:'', x:0, y:0, visible:false})
  // event handlers to take care of entering into a box and exiting

  const handleMouseEnter = (bar: BarInfo, event:MouseEvent<SVGRectElement>) => {
    // setHoverInfo({key:bar.key, x:event.clientX, y:event.clientY,visible:true})
    setHoverInfo({key:bar.key, x:event.nativeEvent.offsetX, y:event.nativeEvent.offsetY,visible:true})
  }
  const handleMouseExit = () => { 
    setHoverInfo({key:'', x:0, y:0, visible:false})
  }

  // get keys excluding the id
  const keys = Object.keys(data[0]).filter((d)=> d!=='playlist_id')
  // define the four scales
  const playlistScale = scaleBand<string>({
    domain: data.map(getID),
    padding: 0.2,
  });
  const genreScale = scaleBand<string>({
    domain: keys,
    padding: 0.1,
  });
  var maxFrequency= Math.max(...data.map((d) => Math.max(...keys.map((key) => Number(d[key])))))
  const frequencyScale = scaleLinear<number>({
    domain: [0, maxFrequency],
  });
  // map a genre to a color
  const colorScale = scaleOrdinal<string, string>({
    domain: keys,
    range: [blue, green, purple],
  });
  // bounds
  const xMax = width - margin.left - margin.right;
  const yMax = height - margin.top - margin.bottom;

  // update scale output dimensions
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
          x0={getID}
          x0Scale={playlistScale}
          x1Scale={genreScale}
          yScale={frequencyScale}
          color={colorScale}
        >
          {(barGroups) =>
            barGroups.map((barGroup) => (
              <Group key={`bar-group-${barGroup.index}-${barGroup.x0}`} left={barGroup.x0}>
                {barGroup.bars.map((bar) => {
                  return (<rect
                  key={`bar-group-bar-${barGroup.index}-${bar.index}-${bar.value}-${bar.key}`}
                  x={bar.x}
                  y={bar.y}
                  width={bar.width}
                  height={bar.height}
                  fill={bar.color}
                  rx={4}
                  onMouseEnter={(event)=> handleMouseEnter(bar, event)}
                  onMouseLeave={handleMouseExit}

                  onClick={() => {
                    if (!events) return;
                    const { key, value } = bar;
                    alert(JSON.stringify({ key, value }));
                  }}
                />);
                }
                  
                )}
              </Group>
            ))
          }
        </BarGroup>
      </Group>
      {hoverInfo.visible && (
      <text
        x={hoverInfo.x-10}
        y={hoverInfo.y-10}
        fill="white"
      >
        {hoverInfo.key}
      </text>
    )}
      <AxisBottom
        top={yMax + margin.top}
        // tickFormat={formatName}
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