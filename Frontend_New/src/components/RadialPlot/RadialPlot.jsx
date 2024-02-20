import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { RadialBar } from '@ant-design/plots';

const RadialPlot = () => {
  const data = [
    {
      name: 'X6',
      star: 297,
    },
    {
      name: 'G',
      star: 506,
    },
  ];
  const config = {
    data,
    xField: 'name',
    yField: 'star',
    maxAngle: 270,
    radius: 0.8,
    innerRadius: 0.6,
    barBackground: {},
    barStyle: {
      lineCap: 'round',
    },
    colorField: 'name',
    color: ({ name }) => {
      if (name === 'screenshot') {
        return 'rgb(255, 171, 0)';
      } else if (name === 'scraping') {
        return 'rgb(0, 167, 111)';
      }

      return '#ff4d4f';
    },
    
  };
  return <RadialBar {...config} />;
};

export default RadialPlot